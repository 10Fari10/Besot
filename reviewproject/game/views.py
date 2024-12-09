from django.shortcuts import render
from django.http import HttpResponse
from game.models import *

from datetime import timezone,timedelta,datetime

import logging
from django.conf import settings

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))


def index(request):
    username = request.user.username
    if UserData.objects.filter(username=username).exists():
        user_data = UserData.objects.filter(username=username).first()
        if user_data and user_data.time!=None:
            time_final = str.zfill(str(int((user_data.time) / 60)),2) +":"+ str.zfill(str(user_data.time % 60),2)
            user_data_list = UserData.objects.all().exclude(time=None).order_by('time')[:10]

            leaderboard = []
            for u in user_data_list:
                t_final= str.zfill(str(int((u.time) / 60)),2) +":"+ str.zfill(str(u.time % 60),2)
                leaderboard.append((u.username, t_final))
            return render(request, "game/completed_screen.html", {'time': time_final, 'leaderboard': leaderboard})
        else:
            render(request, "game/index.html")
    return render(request, "game/index.html")

#Changed my mind
#Times are stored with user data
#Once solution is submitted, lobby name is used to lookup mapdata and compare solution
#If verified, query is made to user table and all users with matching lobby are pulled, sorted by time, and sent

def room(request, room_name):
    mapSolutions = {"alpha":"r1,r2,r3,r4"}
    mapLayouts = {
        "alpha": {
            "r1": {"coords": [43.00235605877655, -78.77763672611523], "hint": "Start here, Clue 1!"},
            "r2": {"coords": [42.999468562433165, -78.79463196260592], "hint": "Clue 2."},
            "r3": {"coords": [42.99849557114192, -78.80136997303279], "hint": "Clue 3."},
            "r4": {"coords": [43.00367421851207, -78.81184178541595], "hint": "Clue 4."}
        }
    }
    #correct_solution_alpha = ["r1", "r2", "r3", "r4"]
    if not request.user.is_authenticated or (room_name not in mapSolutions):
        return HttpResponse('Unauthorized', status=401)
    else:
        #Store map solution by lobby name on load, sample below
        
        #Store and send pin location/id by lobby name on load, sample below
        #if(MapData.objects.filter(lobbyID=room_name).count() ==0):
             map = MapData(lobbyID = room_name, pinLocations = mapLayouts[room_name],solution=mapSolutions[room_name])
             map.save()
             map_layout = mapLayouts[room_name]
             
             return render(request, "game/room.html", {'map_layout': map_layout, 'room_name': room_name})

def completed_screen(request):
    username = request.user.username
    user_data = UserData.objects.filter(username=username).first()
    if user_data:
        time_final = str.zfill(str(int((user_data.time) / 60)),2) +":"+ str.zfill(str(user_data.time % 60),2)
        user_data_list = UserData.objects.all().exclude(time=None).order_by('time')[:10]

        leaderboard = []
        for u in user_data_list:
            t_final = str.zfill(str(int((u.time) / 60)),2) +":"+ str.zfill(str(u.time % 60),2)
            leaderboard.append((u.username, t_final))
    return render(request, "game/completed_screen.html", {'time': time_final,'leaderboard': leaderboard})