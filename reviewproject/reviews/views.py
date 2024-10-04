from django.shortcuts import render


def main_homepage(request):
    return render(request, 'reviews/homepage.html') 



# Create your views here.