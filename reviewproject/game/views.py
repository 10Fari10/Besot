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
    username = request.user.username
    mapSolutions = {"alpha":"r1,r2,r3,r4,r5,r6,r7,r8"}
    mapLayouts = {
        "alpha": {
            "r1": {"coords": [43.001989124349436, -78.78949571846864], "hint": "STARTING POINT! Go to the building that is the tallest in Buffalo!"},
            "r2": {"coords": [42.886729425585564, -78.87927135895511], "hint": "Go to the place where the South meets the North."},
            "r3": {"coords": [42.907181648776465, -78.90596614545902], "hint": "Go to the place where we meet 3 times a week at 3pm."},
            "r4": {"coords": [43.00283907952901, -78.78720185895041], "hint": "Go to the noisiest library of UB."},
            "r5": {"coords": [43.00103504664003, -78.78954004545508], "hint": "Go to the home of the favorite football team of Buffalo."},
            "r6": {"coords": [42.77398295750286, -78.78692938779457], "hint": "Go to the park where a sculpture of a great man stands."},
            "r7": {"coords": [42.90547599646025, -78.83963908778925], "hint": "Go to a place in UB where you can see entertaining performences."},
            "r8": {"coords": [43.00107826409083, -78.78289954928323], "hint": "Finish!."}
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
        user_data = UserData.objects.filter(username=username).first()
        if user_data and user_data.time!=None:
            return render(request, 'reviews/homepage.html')
        else:
            return render(request, "game/room.html", {'map_layout': map_layout, 'room_name': room_name})

def completed_screen(request):
    username = request.user.username
    user_data = UserData.objects.filter(username=username).first()
    time_final
    if user_data:
        time_final = str.zfill(str(int((user_data.time) / 60)),2) +":"+ str.zfill(str(user_data.time % 60),2)
        user_data_list = UserData.objects.all().exclude(time=None).order_by('time')[:10]

        leaderboard = []
        for u in user_data_list:
            t_final = str.zfill(str(int((u.time) / 60)),2) +":"+ str.zfill(str(u.time % 60),2)
            leaderboard.append((u.username, t_final))
        return render(request, "game/completed_screen.html", {'time': time_final,'leaderboard': leaderboard})