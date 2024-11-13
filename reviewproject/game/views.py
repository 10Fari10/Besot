from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from game.models import *
import json

import logging
from django.conf import settings

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))

def index(request):
    return render(request, "game/index.html")

#Changed my mind
#Times are stored with user data
#Once solution is submitted, lobby name is used to lookup mapdata and compare solution
#If verified, query is made to user table and all users with matching lobby are pulled, sorted by time, and sent
def room(request, room_name):
    #Store map solution by lobby name on load, sample below
    mapSolutions = {"alpha":"r1,r2,r3,r4"}
    #Store and send pin location/id by lobby name on load, sample below
    mapLayouts = {"alpha":json.dumps({"r1":[1,2],"r2":[2,3],"r3":[4,2]})}
    map = MapData(lobbyID = room_name, pinLocations = mapLayouts[room_name],solution=mapSolutions[room_name])
    map.save()
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    else:
        return render(request, "game/room.html", {"room_name": room_name,"map_layout":mapLayouts[room_name]})