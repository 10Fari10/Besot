
from django.urls import path
from reviews.views import main_homepage

urlpatterns = [path('', main_homepage, name='main_homepage'),] 