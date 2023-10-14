from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = "accounts"

urlpatterns = [
    
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    #path("login/", login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    #### Password reset  ###
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    path("reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_complete.html"), name="password_reset_done"),
    #path("reset_password_confirmation/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_confirmation.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/ ", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_confirmation.html"), name="password_reset_confirmation"), 
    path("reset_password_done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_confirmation.html"), name="password_reset_done"),
   
    ### password change ###
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="pass-change"),
    path("change_complete/", auth_views.PasswordChangeDoneView.as_view(template_name="accounts/change-complete.html"), name="change-complete"),
    
    path("register/", SignUp, name="signup"),
    path("", home, name="home"),
    path("welcome", home_page, name="home-page"),
    path("aboutus/", aboutus, name="about-us"),
    path("contact/", contact, name="contact"),
    path("business/", home_business.as_view(), name="home-business"),
    #path("experts/", home_expert.as_view(), name="home-expert"),
    path("employee/", home_business.as_view(), name="home-employee"),
    path("admin/", home_admin.as_view(), name="home-admin"),
    path("privacy_policy/", privacy, name="privacy"),
    path("terms_and_conditions/", conditions, name="conditions"),
    path("services/", services, name="service"),
    path("packages/", packages, name="package"),
]
    
    
