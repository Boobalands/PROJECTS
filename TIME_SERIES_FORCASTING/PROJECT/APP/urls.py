from django.urls import path
from . import views

urlpatterns =[
    
    path('', views.Landing_1, name='Landing_1'),
    path('Register_2/', views.Register_2, name='Register_2'),
    path('Login_3/', views.Login_3, name='Login_3'),
    path('Home_4', views.Home_4, name='Home_4'),
    path('Teamates_5/', views.Teamates_5, name='Teamates_5'),
    path('Per_Info_6/', views.Per_Info_6, name='Per_Info_6'),
    path('Per_Database_7/', views.Per_Database_7, name='Per_Database_7'),
    path('Deploy_8/', views.Deploy_8, name='Deploy_8'),
    path('Deploy_9/', views.Deploy_9, name='Deploy_9'),
    path('Logout/', views.Logout, name='Logout'),
]