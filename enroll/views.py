from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
import uuid
from .forms import profile_admin,profile_user,Profileimage
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import  SetPasswordForm

# signup
def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        try:
            if User.objects.filter(username=username).first():
                messages.info(request, "User already exist")
                return redirect('sign')
            if User.objects.filter(email=email).first():
                messages.info(request, "Email already exist")
                return redirect('sign')
            user_obj = User(username=username, email=email, first_name=name)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            Email_send_register(email, auth_token)
            return redirect('/token')
        except Exception as e:
            print(e)

    return render(request, 'signup.html')


# login for
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.info(request, "User not found ?")
            return redirect('login')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verify:
            messages.info(request, "Account not verified ,Check mail")
            return redirect('login')

        user = authenticate(request, username=username, password=request.POST['password'])
        # if user is not None:
        #     login(request,user)
        #     messages.info(request, 'Login Successfully ! Now enjoy app ')
        #     return redirect('/')
        if user is None:
            messages.info(request, "Wrong password...")
            return redirect('login')
        login(request, user)
        messages.info(request, "logged in...")
        return redirect('/')
    return render(request, 'login.html')

#
# ##register
# ##success
# def success(request):
#     return render(request, 'success.html')
#

# token
def token_send(request):
    return render(request, 'token_send.html')


##Error
def Error(request):
    return render(request, 'errors.html')


##verify email
def Email_verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verify:
                messages.success(request, 'Email already verified ! Now can can login the site')
                return redirect('login')
            else:
                profile_obj.is_verify = True
                profile_obj.save()
                messages.success(request, 'Email verified successful ! now can can login the site')
                return redirect('login')

        else:
            return redirect('/errors')
    except Exception as e:
        print(e)


##email_send
def Email_send_register(email, auth_token):
    subject = 'Your accounts to be verify'
    message = f"Hi paste the link to verify your account http://127.0.0.1:8000/verify/{auth_token}"
    email_from = settings.EMAIL_HOST_USER
    to = email
    send_mail(subject, message, email_from, [to], fail_silently=False)


##Dashboard
# @login_required(login_url='login')
# def Home(request):
#     return render(request, 'profile.html')
#

#profile
@login_required(login_url='login')
def Home(request):
    try:
        pst_data=request.POST or None
        file_data=request.FILES or None
        pro_obj=Profileimage(pst_data,file_data,instance=request.user.profile)
        if pro_obj.is_valid():
            pro_obj.save()
            messages.success(request,'Profile picture updated')
            return redirect('home')
        return render(request, 'profile.html',{'pro_obj':pro_obj})
    except Exception as e:
        print(e)




##logged out
def user_logout(request):
      logout(request)
      messages.success(request,'User logout')
      return HttpResponseRedirect("/login/")

#
# ##forget password
# def Forget_pass(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         print(email)
#         subject = 'Password reset request from technos app'
#         message = f"Hi paste the link to verify your account http://127.0.0.1:8000/success/"
#         email_from = settings.EMAIL_HOST_USER
#         to = email
#         send_mail(subject, message, email_from, [to], fail_silently=False)
#         return redirect('/success')
#     return render(request,'forget_pass.html')

###change password inside dashboard
def user_change1(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.info(request, 'Password changed ! ')
                return redirect('home')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request, 'change1.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login')


###Profile_detail
def Profile_detail(request):
    return render(request,'profile_detail.html')


###profile_update
def Profile_update(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser == True:
                fm = profile_admin(request.POST, instance=request.user)
                user = User.objects.all()
            else:
                fm = profile_user(request.POST, instance=request.user)
                user = None
            if fm.is_valid():
                fm.save()

                return redirect('profile')
        else:
            if request.user.is_superuser == True:
                fm = profile_admin(instance=request.user)
                user = User.objects.all()
            else:

                fm = profile_user(instance=request.user)
                user = None
        return render(request, 'profile_update.html', {'fm': fm, 'user': user})
    else:
        return redirect('profile')
