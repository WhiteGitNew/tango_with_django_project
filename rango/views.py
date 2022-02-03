from cgitb import html
from re import A
from django.shortcuts import render

from django.http import HttpResponse
from django.template import context

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # 将模板变量名template variable 映射到python变量
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request,'rango/index.html',context=context_dict)
    #render函数接收用户的request, 模板html文件和 context键值对字典

    #return HttpResponse("Rango says hey there partner!<a href='/rango/about/'>About</a>")
    


def about(request):
    #return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")

    context_dict = {}
    return render(request,'rango/about.html',context=context_dict)