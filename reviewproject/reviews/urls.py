
from django.urls import path

from reviews.views import *

urlpatterns = [
    path('', main_homepage, name='main_homepage'),
    path("send_post/",sendPost,name='send_post/'),
    path("map_post/",postHandle,name='map_post/'),
    path("like/",likeHandle,name='like/'),
    path("pins/",sendPins,name="pins/"),
    path("pfp_load",loadpfp,name="pfp_load"),
    path("pfp_post",postpfp,name="pfp_post"),
    ] 