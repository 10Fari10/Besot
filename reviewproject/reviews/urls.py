
from django.urls import path
from reviews.views import *

urlpatterns = [
    path('', main_homepage, name='main_homepage'),
    path('test/',db_test,name = 'test/'),
    path('show/',show,name = 'show/')
    ] 