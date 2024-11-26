import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from game.models import *

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
         
        text_data_json = json.loads(text_data)
        if "solution" in text_data_json.keys():
            solution = text_data_json["solution"]
            room = text_data_json["room"]
            time = text_data_json["tim"]
            tim = time
            time = time.split(":")
            min = time[0]
            seconds = time[1]
            tens = time[2]
            if min[0] == '0':
                min = min[1:]
            if seconds[0] == '0':
                seconds = seconds[1:]
            if tens[0] == '0':
                tens = tens[1:]
            min = int(min)
            second = int(seconds)
            ten = int(tens)
            total_time = min * 60
            total_time = total_time * 10
            t = second * 10
            total_time = t + total_time + ten
            user = self.scope["user"].username

            logging.debug(f"User-room: {room}")
            logging.debug(f"User-solution: {solution}")
            map_data = MapData.objects.filter(lobbyID=room).first()
            if map_data:
                map_solution = map_data.solution.split(',')
                user_solution = solution.split(',')
                if user_solution == map_solution:
                    record = UserData(username=user, lobby=room, time=total_time)
                    record.save()
                    user_data_list = UserData.objects.all().order_by('time')[:10]
                    self.send(text_data=json.dumps({"correct": True, "redirect": "completed_screen"}))
                    logging.debug("Correct solution")
                else:
                    user_data_list = UserData.objects.all().order_by('time')[:10]
                    self.send(text_data=json.dumps({"correct": False, "reset": True}))
                    logging.debug("Incorrect solution")
                # if UserData.objects.filter(lobby=room, username=user).count() == 0:
                #     logging.debug("New record for user")
                #     record = UserData(username=user, lobby=room, time=tim, total_time=total_time)
                #     record.save()
                # else:
                #     record = UserData.objects.get(lobby=room, username=user)
                #
                # if record.time is None:
                #     record.time = 1
                #     record.save()

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
            min = int(text_data_json["min"])
            sc = int(text_data_json["sc"])
            tns = int(text_data_json["tns"])
            tns += 1
            if tns > 9 :
                tns = 0
                sc += 1
            if sc > 59:
                sc = 0
                min += 1
            min = str(min)
            sc = str(sc)
            tns = str(tns)
            if len(min) == 1:
                min = "0" + min
            if len(sc) == 1:
                sc = "0" + sc
            if len(tns) == 1:
                tns = "0" + tns
            user_data_list = UserData.objects.all().order_by('time')[:10]
            username = []
            t = []
            for u in user_data_list:
                username.append(u.username)
                time_con = u.time
                m = time_con // 600
                s  = (time_con % 600) // 10
                c = time_con % 10
                m = str(m)
                s = str(s)
                c = str(c)
                if len(m) == 1 :
                    m = "0" + m
                if len(s) == 1 :
                    s = "0" + s
                if len(c) == 1 :
                    c = "0" + c
                time_final = m + ":" + s +":" + c
                t.append(time_final)
            self.send(text_data=json.dumps({"min": min, "sc": sc , "tns":  tns, "leader_user": username, "leader_time": t}))

    def chat_message(self, event):
        rankings = event["rankings"]
        self.send(text_data=json.dumps({"rankings": rankings}))