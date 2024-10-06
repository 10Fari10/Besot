from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from reviews.models import Users
from django.views.decorators.csrf import csrf_protect

def main_homepage(request):
    return render(request, 'reviews/homepage.html') 

@csrf_protect
def db_test(request):
    user = Users(username="wa",password= "aef",salt="gs")
    user.save()
    next = request.POST.get('next','/')
    return HttpResponseRedirect(next)

@csrf_protect
def show(request):
  myusers = Users.objects.all().values()
  template = loader.get_template('reviews/test.html')
  context = {
    'tests': myusers,
  }
  return HttpResponse(template.render(context, request))