
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main_homepage, name='main_homepage'),
    path("send_post/",views.sendPost,name='send_post/'),
    path("map_post/",views.postHandle,name='map_post/'),
    path("like/",views.likeHandle,name='like/'),
    path("pins/",views.sendPins,name="pins/"),
    path("pfp_load",views.loadpfp,name="pfp_load"),
    path("pfp_post",views.postpfp,name="pfp_post"),


    ]