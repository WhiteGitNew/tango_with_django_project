from cgitb import html
from re import A
from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there partner!<a href='/rango/about/'>About</a>")
    #return HttpResponse("<a href='/rango/about/'>Rango says hey there partner!</a>")
def about(request):
    return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")
    #return HttpResponse("<a href='/rango/'>Rango says here is the about page.</a>")