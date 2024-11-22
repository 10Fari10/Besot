
from django.urls import path


from reviews.views import *
from game.views import *

urlpatterns = [
    path('', main_homepage, name='main_homepage'),
    path("send_post/",sendPost,name='send_post/'),
    path("map_post/",postHandle,name='map_post/'),
    path("like/",likeHandle,name='like/'),
    path("pins/",sendPins,name="pins/"),
    path("pfp_load",loadpfp,name="pfp_load"),
    path("pfp_post",postpfp,name="pfp_post"),
    path('get_map_layout/<str:room_name>/', room, name='get_map_layout'),
    path('completed_screen/', completed_screen, name='completed_screen'),
    ] 