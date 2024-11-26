from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from game.models import *
import json
import time

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
        if user_data:
            time_user = user_data.time
            m = time_user // 600
            s = (time_user % 600) // 10
            c = time_user % 10
            m = str(m)
            s = str(s)
            c = str(c)
            if len(m) == 1:
                m = "0" + m
            if len(s) == 1:
                s = "0" + s
            if len(c) == 1:
                c = "0" + c
            time_final = m + ":" + s + ":" + c
            user_data_list = UserData.objects.all().order_by('time')[:10]

            leaderboard = []
            for u in user_data_list:

                time_con = u.time
                m = time_con // 600
                s = (time_con % 600) // 10
                c = time_con % 10
                m = str(m)
                s = str(s)
                c = str(c)
                if len(m) == 1:
                    m = "0" + m
                if len(s) == 1:
                    s = "0" + s
                if len(c) == 1:
                    c = "0" + c
                t_final = m + ":" + s + ":" + c
                leaderboard.append((u.username, t_final))
        return render(request, "game/completed_screen.html", {'time': time_final, 'leaderboard': leaderboard})
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

# def getLeaderboards(request):
#     if not request.user.is_authenticated:
#         return HttpResponse('Unauthorized', status=401)
#     users = UserData.objects.filter(time__isnull=False).order_by('time')[:10]
#     if len(users) < 10:
#         users = UserData.objects.filter(time__isnull=False).order_by('time')
#     if len(users) >0:
#         return render(request, "game/room.html", {'leaderboard': users})
#     else:
#         return render(request, "game/index.html", {'message': 'No users found'})
#
#

def completed_screen(request):
    username = request.user.username
    user_data = UserData.objects.filter(username=username).first()
    if user_data:
        time_user = user_data.time
        m = time_user // 600
        s = (time_user % 600) // 10
        c = time_user % 10
        m = str(m)
        s = str(s)
        c = str(c)
        if len(m) == 1:
            m = "0" + m
        if len(s) == 1:
            s = "0" + s
        if len(c) == 1:
            c = "0" + c
        time_final = m + ":" + s + ":" + c
        user_data_list = UserData.objects.all().order_by('time')[:10]

        leaderboard = []
        for u in user_data_list:

            time_con = u.time
            m = time_con // 600
            s = (time_con % 600) // 10
            c = time_con % 10
            m = str(m)
            s = str(s)
            c = str(c)
            if len(m) == 1:
                m = "0" + m
            if len(s) == 1:
                s = "0" + s
            if len(c) == 1:
                c = "0" + c
            t_final = m + ":" + s + ":" + c
            leaderboard.append((u.username, t_final))
    return render(request, "game/completed_screen.html", {'time': time_final,'leaderboard': leaderboard})