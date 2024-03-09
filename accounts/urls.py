from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = "accounts"

urlpatterns = [

    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name="accounts/login.html"), name="logout"),

    #### Password reset  ###
    path("reset-password/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password-reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password-reset-done"),
    path("reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_complete.html"), name="password_reset_done"),
    #path("reset_password_confirmation/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_confirmation.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/ ", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_confirmation.html"), name="password_reset_confirmation"),


    ### password change ###
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="pass-change"),
    path("change_complete/", auth_views.PasswordChangeDoneView.as_view(template_name="accounts/change-complete.html"), name="change-complete"),

    ### Site links ###
    #path('logout/', logout_view, name='logout'),
    #path("register/", SignUp, name="signup"),
    #path("register/", signup, name="signup"),
    path("register/", register, name="signup"),
    path("", home, name="home"),
    path("testing", testing, name="testing"),
    path("welcome", home_page, name="home-page"),
    #path("welcome", HomePageView.as_view(), name="home-page"),
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
    path("stats/", stats, name="stats"),

    ### Work Experience
    path("work_experience/", WorkExperienceListView.as_view(), name="experience-list"),
    path("work_experience/create/", WorkExperienceCreateView.as_view(), name="experience-create"),
    path('work_experience/<int:pk>/update/', WorkExperienceUpdateView.as_view(), name='experience-update'),

    ### Exper Portfolio
    path("expert_portfolio/", ExpertPortfolioListView.as_view(), name="portfolio-list"),
    path("expert_portfolio/create/", ExpertPortfolioCreateView.as_view(), name="portfolio-create"),
    path('portfolio/<int:pk>/update/', ExpertPortfolioUpdateView.as_view(), name='portfolio-update'),
    ### Work Experience
    path("education/", EducationListView.as_view(), name="education-list"),
    path("education/create/", EducationCreateView.as_view(), name="education-create"),
    path('education/<int:pk>/update/', EducationUpdateView.as_view(), name='education-update'),

    path("admin-register/", AdminSignUp, name="admin-signup"),
    path("employee-register/", EmployeeSignUp, name="employee-signup"),

    ### Read content ###
    path("content-read/", ReadContentView.as_view(), name="content-read" ),

    ##### Email verification ###
    #path('verify-email/', verify_email, name='verify-email'),
    path('verify-email/done/', verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify-email-complete'),
    #path('verify-email-confirm/<uidb64>/<token>/', activate, name='verify-email-confirm'),
    #path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('verify-email/', initial_registration, name='verify-email'),

]


