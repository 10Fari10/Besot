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
     room = text_data_json["room"]
     user = self.scope["user"].username

     logging.debug(f"User-room: {room}")
     logging.debug(f"User-solution: {solution}")

    
     map_data = MapData.objects.filter(lobbyID=room).first()

     if map_data:
        map_solution = map_data.solution.split(',')
        user_solution = solution.split(',')

        if user_solution == map_solution:
            self.send(text_data=json.dumps({"correct": True, "redirect": "completed_screen"}))
            logging.debug("Correct solution")
        else:
           
            self.send(text_data=json.dumps({"correct": False, "reset": True}))
            logging.debug("Incorrect solution")

        
        if UserData.objects.filter(lobby=room, username=user).count() == 0:
            logging.debug("New record for user")
            record = UserData(username=user, lobby=room, time=None)
            record.save()
        else:
            record = UserData.objects.get(lobby=room, username=user)

        if record.time is None:
            record.time = 1  
            record.save()

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
    def chat_message(self, event):
        rankings = event["rankings"]
        self.send(text_data=json.dumps({"rankings": rankings}))