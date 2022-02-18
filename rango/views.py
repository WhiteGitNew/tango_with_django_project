from audioop import reverse
from cgitb import html
import profile
from re import A
from django.shortcuts import redirect, render
from django.urls import reverse


from django.template import context
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):

    #query 数据库中的categories,按降序排列top5,将list放在context字典中
    category_list = Category.objects.order_by('-likes')[:5]
    #query pages, 选取top5
    pages_list = Page.objects.order_by('-views')[:5]

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # 将模板变量名template variable 映射到python变量, 存在dict数据结构中

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

@login_required
def add_category(request):
    form = CategoryForm()

    #是否是http POST请求
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #form 是否有效？
        if form.is_valid():
            cat = form.save(commit=True)
            print (cat,cat.slug)
            return redirect('/rango/')
            #返回网页
        else:
            print(form.errors)
    return render(request,'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    #检查cate是否存在
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs = {'category_name_slug':
                                                  category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category':category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    # bool值 注册是否成功
    registered = False

    if request.method == 'POST':
        #尝试从生表格中收集数据
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #如果valid 储存数据
            user = user_form.save()

            #hash password, update user object
            user.set_password(user.password)
            user.save()

            #sort out the userprofile instance
            #commit=false 来推迟model储存
            profile = profile_form.save(commit=False)
            profile.user = user

            #上传图片
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save

            registered = True
        else:
            #不可用表格
            print(user_form.errors, profile_form.errors)
    else:
        #如果不是HTTP POST请求,空白表格
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'rango/register.html',
                           context={'user_form': user_form,
                                    'profile_form': profile_form,
                                    'registered': registered})
def user_login(request):
    if request.method == 'POST':
        #收集从用户提供的用户名密码,通过login表单
        username = request.POST.get('username')
        password = request.POST.get('password')

        #用django自带的机制检查用户密码对,返回obj
        user = authenticate(username=username,password=password)

        # 如果得到了user obj 那么正确
        # 如果没得到obj, None 找不到user
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('rango:index'))
            else:
                #非活跃用户
                return HttpResponse("Your Rango account is disabled.")
        else:
            # 提供信息不正确
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    #如果不是http request请求, 展示登录表格
    #这种场景很可能是HTTP get
    else:
        return render(request, 'rango/login.html')
    

@login_required
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html')

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))
