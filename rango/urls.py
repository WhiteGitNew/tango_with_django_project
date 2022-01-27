from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    #如果匹配到'' 那么调用views.index, index是对view的convention
]