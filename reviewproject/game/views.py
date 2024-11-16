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

#43.00235605877655 map.js:28:25
# -78.77763672611523 map.js:29:25
# 42.999468562433165 map.js:28:25
# -78.79463196260592 map.js:29:25
# 42.99849557114192 map.js:28:25
# -78.80136997303279 map.js:29:25
# 43.00367421851207 map.js:28:25
# -78.81184178541595 map.js:29:25
# 42.995545116259315 map.js:28:25
# -78.77999717562783
def room(request, room_name):
    mapSolutions = {"alpha":"r1,r2,r3,r4"}
    mapLayouts = {"alpha":json.dumps({"r1":[43.00235605877655,-78.77763672611523],
                                      "r2":[42.999468562433165,-78.79463196260592],
                                      "r3":[42.99849557114192,-78.80136997303279]})}
    if not request.user.is_authenticated or (room_name not in mapSolutions):
        return HttpResponse('Unauthorized', status=401)
    else:
        #Store map solution by lobby name on load, sample below
        
        #Store and send pin location/id by lobby name on load, sample below
        if(MapData.objects.filter(lobbyID=room_name).count() ==0):
            map = MapData(lobbyID = room_name, pinLocations = mapLayouts[room_name],solution=mapSolutions[room_name])
            map.save()
        return render(request, "game/room.html", {"room_name": room_name,"map_layout":mapLayouts[room_name]})
def getLeaderboards(request):
    if not request.user.is_authenticated :
        return HttpResponse('Unauthorized', status=401)
    users = UserData.objects.filter(time__isnull=False).order_by('time')[:10]
    if len(users) < 10:
        users = UserData.objects.filter(time__isnull=False).order_by('time')

    return render(request, "game/room.html", {'leaderboard': users})
