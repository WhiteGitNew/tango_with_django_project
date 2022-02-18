from unicodedata import name
from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    #如果匹配到'' 那么调用views.index, index是对view的convention
    path('about/', views.about, name='about'),
    #如果匹配到about/,那么调用about界面

    #slug变量用来mapping, 由show_category view传
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),

    path('add_category/', views.add_category, name='add_category'),

    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]