from cgitb import html
from re import A
from django.shortcuts import render

from django.http import HttpResponse
from django.template import context
from rango.models import Category
from rango.models import Page


def index(request):

    #query 数据库中的categories,按降序排列top5,将list放在context字典中
    category_list = Category.objects.order_by('-likes')[:5]
    #query pages, 选取top5
    pages_list = Page.objects.order_by('-views')[:5]

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # 将模板变量名template variable 映射到python变量

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list

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

#用来添加新page给每个category
def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    # 创建context字典来传给template引擎
    context_dict = {}

    try:
        #是否能找到所给名字的category name slug?
        #如果找不到,the .get() method raises a DoesNotExist exception.
        #如果找到,get返回实例model
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        #遍历所有相关page,使用filter
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        #同时将cat实例从数据库加载到context字典中,可以用来在template中证实cat存在
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)
