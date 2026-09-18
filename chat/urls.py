from django.urls import path
from .views import *
urlpatterns =[
    path('register',register_view,name='register'),
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout'),
    path('',home_view,name='home'),
    path('room/<str:room_name>/',room_view,name='room'),
]