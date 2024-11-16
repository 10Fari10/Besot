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
        solution = text_data_json["solution"]
        room =  text_data_json["room"]
        user = self.scope["user"].username
        logging.debug("User-room:"+room)
        logging.debug("User-solution:"+solution)
        logging.debug(MapData.objects.all().values())
        #Check if map is valid
        if(MapData.objects.filter(lobbyID=room).count() ==1):
            map = MapData.objects.get(lobbyID=room)
            logging.debug("Map-sol"+map.solution)
            #Check if user record already exists, create if it doesn't
            if (UserData.objects.filter(lobby=room,username=user).count() ==0):
                logging.debug("new record")
                record = UserData(username=user,lobby=room,time=None)
                record.save()
            else:
                record = UserData.objects.get(lobby=room,username=user)

            #If user already has time, do not update 
            if(record.time is None):    
                if map.solution == solution:
                    logging.debug("correct")
                    record.time = 1
                    record.save()
        #Send all rankings
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

    def chat_message(self, event):
        rankings = event["rankings"]
        self.send(text_data=json.dumps({"rankings": rankings}))