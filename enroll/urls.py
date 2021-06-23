from django.contrib import admin
from django.urls import path
from enroll import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.Home, name='home'),
    path("profile/profile_detail/", views.Profile_detail, name='profile'),
    path("profile/profile_update/", views.Profile_update, name='profileup'),
    path("login/",views.login_user,name="login"),
    path("sign/",views.sign_up,name="sign"),
    path("token/",views.token_send,name="token"),
    #path("success/", views.success, name="success"),
    path("verify/<slug:auth_token>",views.Email_verify,name='verify'),
    path("errors/",views.Error,name='errors'),
    path('user_logout/',views.user_logout,name="user_logout"),
   # path("forget_pass/",views.Forget_pass,name='forget_pass'),
    path('profile/change1/', views.user_change1, name='change1'),

###for reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
]
