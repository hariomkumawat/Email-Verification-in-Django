from django.shortcuts import render

# Create your views here.
from .models import *
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import Settings,settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def home(request):
    return render (request,('home.html'))






def login_attempt(request):
 try:
    if request.method == 'POST':
        username = request.POST.get('username')
        #email = request.POST.get('email')
        password= request.POST.get('password')
        if not username or not password:
            messages.success(request, 'Both username and Password are required.')
            return redirect('/login')
        user_obj=User.objects.filter(username =username).first()
        if user_obj is None:
            messages.success(request, 'User Not Found.')
            return redirect('/login')

        profile_obj =Profile.objects.filter(user=user_obj).first()
        # sed mail code
        if not profile_obj.is_verifyed:
            messages.success(request, 'Profile is not verified check your mail .')
            return redirect('/login')
            ###
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request, 'Worng Password !!.')
            return redirect('/login')
        login(request,user)
        return redirect('/')
 except Exception as e:
    print(e)
 return render (request,('login.html'))



def register_attempt(request):
 try:
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password= request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is Alread Exists.')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is Alread Exists.')
                return redirect('/register')
            user_obj =User.objects.create(username =username,email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token =str(uuid.uuid4())
            profile_obj =Profile.objects.create(user =user_obj ,auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect ('/token')
        except Exception as e :
            print(e)
 except Exception as e :
        print(e)
 return render (request,('register.html'))


def success(request):
    return render (request,('success.html'))

def token_send(request):
    return render (request,('token_send.html'))

def Logout(request):
    logout(request)
    return redirect ('/login')


def ForgetPassword(request):
    try:
        if request.method =='POST':
            username =request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request, 'User Not  Found with the username .')
                return redirect('/forget_password/')
            else:
                pass_obj =User.objects.get(username =username)
                # forget_password_token =str(uuid.uuid4())
                # profile_obj =Profile.objects.create(user= pass_obj,forget_password_token=forget_password_token)
                # profile_obj.save()
                # send_forget_password_mail(pass_obj.email ,forget_password_token)
                token = str(uuid.uuid4())
                # print(token)
                profile_obj =Reset.objects.create(user= pass_obj)
                profile_obj.forget_password_token = token
                profile_obj.save()
                # token.save()
                send_forget_password_mail(pass_obj.email,token)
                messages.success(request, 'An email is send Please check the email and click to reset password .')
                return redirect('/forget_password/')
    except Exception as e :
       print (e)
    return render (request,"forget_password.html")

def ChangePassword(request,token):
    context ={}
    try:
        profile_obj = Reset.objects.filter(forget_password_token= token).first()
        context={'user_id':profile_obj.user.id}
        print(profile_obj)
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password= request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')
            print(user_id)
            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change_password/{token}/')

            if  new_password !=  confirm_password :
                messages.success(request, 'Both should be equal.')
                return redirect(f'/change_password/{token}/')
            user_obj= User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login')

    except Exception as e:
        print (e)
    return render (request,"change_password.html",context)



def verify(request, auth_token):
    try:
        profile_obj =Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verifyed:
                messages.success(request, 'Your  Account has been Already  Verified !!.')
                return redirect('/login')
            profile_obj.is_verifyed =True
            profile_obj.save()
            messages.success(request, 'Your  Account has been Verified . Successfully !!.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)






def send_mail_after_registration(email,token):
    subject = "Your Account to be Verified"
    message = f"Hi paste the link to verify Your Account http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)



def send_forget_password_mail(email,token):
    subject = "Your Forget Password link"
    message = f"Hi, Click on the link to reset  Your Password   http://127.0.0.1:8000/change_password/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)



