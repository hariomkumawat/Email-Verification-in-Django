from django.contrib.messages.api import error
from django.urls import path
from .views import *
urlpatterns = [
    path('',home ,name='home'),
    path('register',register_attempt ,name='register_attempt'),
    path('login',login_attempt ,name='login_attempt'),
    path('success',success ,name='success'),
    path('token',token_send ,name='token_send'),
    path('verify/<auth_token>',verify,name='verify'),
    path ('forget_password/',ForgetPassword,name='forget_password'),
    path ('change_password/<token>',ChangePassword,name='change_password'),
    path ('logout/',Logout,name='logout'),

]
