import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from game.models import *

from datetime import timezone,timedelta,datetime

import logging
from django.conf import settings

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "game_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    
    #Receive user solutions. Check solution, update database, and send new rankings
    def receive(self, text_data):
        username = self.scope["user"].username
        logging.debug(username)
        text_data_json = json.loads(text_data)
        room = text_data_json["room"]

        if(UserData.objects.filter(username=username).count() == 0):
            start = datetime.now(timezone.utc)
            user = UserData(username=username, lobby=room, time=None,start=start)
            user.save()
        else:
            user = UserData.objects.filter(username=username).first()

        if "solution" in text_data_json.keys():
            solution = text_data_json["solution"]
            
            logging.debug(f"User-room: {room}")
            logging.debug(f"User-solution: {solution}")

            map_data = MapData.objects.filter(lobbyID=room).first()
            if map_data:
                map_solution = map_data.solution.split(',')
                user_solution = solution.split(',')
                if user_solution == map_solution:
                    total_time = (datetime.now(timezone.utc) - user.start).seconds
                    user.time = total_time
                    user.save()
                    user_data_list = UserData.objects.all().order_by('time')[:10]
                    self.send(json.dumps({"correct": True, "redirect": "completed_screen"}))
                    logging.debug("Correct solution")
                else:
                    user_data_list = UserData.objects.all().order_by('time')[:10]
                    self.send(json.dumps({"correct": False, "reset": True}))
                    logging.debug("Incorrect solution")

            # Get rankings and send them
                rankingsDB = UserData.objects.filter(lobby=room).exclude(time=None).order_by("time").values()
                rankings = []
                for r in rankingsDB:
                    place = {}
                    place["user"] = r["username"]
                    place["lobby"] = r["lobby"]
                    place["time"] = r["time"]
                    rankings.append(place)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, { "type": "chat_message","rankings": rankings}
                )
        else:
            elapsed_time = (datetime.now(timezone.utc) - user.start).seconds
            min = int(elapsed_time / 60)
            sc= elapsed_time % 60
            logging.debug("ELAPSED")
            logging.debug(elapsed_time)
            logging.debug(min)
            logging.debug(sc)
         
            user_data_list = UserData.objects.all().exclude(time=None).order_by('time')
            user_current = UserData.objects.filter(time=None).order_by('-start')
            username = []
            t = []
            for u in user_data_list:
                username.append(u.username)
                l_min = int(u.time / 60)
                l_sc= u.time % 60
                l_time_final = str.zfill(str(l_min),2) +":"+ str.zfill(str(l_sc),2)
                t.append(l_time_final)
            
            for u in user_current:
                other_elapsed_time = (datetime.now(timezone.utc) - u.start).seconds
                other_min = int(elapsed_time / 60)
                other_sc= other_elapsed_time % 60

                username.append(u.username)
                other_time_final = str.zfill(str(other_min),2) +":"+ str.zfill(str(other_sc),2)
                t.append(other_time_final)
            logging.debug(json.dumps({"min": min, "sc": sc, "leader_user": username[:10], "leader_time": t[:10]}))
            self.send(json.dumps({"time":True,"min": min, "sc": sc, "leader_user": username[:10], "leader_time": t[:10]}))

    def chat_message(self, event):
        rankings = event["rankings"]
        self.send(text_data=json.dumps({"rankings": rankings}))
    