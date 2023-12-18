from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
#from products.views import CreateCheckoutSessionView
from core.models import *
#### MFA #######
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
#from rest_framework_simplejwt.views import TokenOBtainPairView, TokenRefreshView, TokenVerifyView

### class for MFA usage, this will help create the MFA site for user
class OTPAdmin(OTPAdminSite):
   pass

admin_site = OTPAdmin(name='OTPAdmin')
#admin_site.register(CustomUser)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)


urlpatterns = [
    #path('api-auth/', include('rest_framework.urls')),
    #path('create-checkout-session',CreateCheckoutSessionView.as_view(),name = 'create-checkout-session'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('manage/', admin.site.urls),
    ### using MFA ###
    #path('manage/', admin_site.urls),
    
    path('', include('accounts.urls', namespace='accounts')),
    path("contacts/", include('contacts.urls', namespace="contacts")),
    
    path("profiles/", include('profiles.urls', namespace="profiles")),
    path("industries/", include('industries.urls', namespace="industries")),
    path("fiches/", include('fiches.urls', namespace="fiches")),
    path("jobs/", include('jobs.urls', namespace="jobs")),
    path("testimonies/", include('testimonies.urls', namespace="testimonies")),
    path("applications/", include('applications.urls', namespace="applications")),
    path("blogs/", include('blogs.urls', namespace="blogs")),
    path("deals/", include('deals.urls', namespace="deals")),
    path("rfi/", include('rfi.urls', namespace="rfi")),
    path("projects/", include('projects.urls', namespace="projects")),
    path("enterprises/", include('enterprises.urls', namespace="enterprises")),
    
    path('tinymce/', include('tinymce.urls')), #add this
    path("trainings/", include('trainings.urls', namespace="trainings")),
    path("trainingapplications/", include('trainingapplications.urls', namespace="trainingapplications")),
    path("analytics/", include('analytics.urls', namespace="analytics")),
    path("product_deals/", include('product_deals.urls', namespace="product_deals")),
    path("discussions/", include('discussions.urls', namespace="discussions")),
    path("products/", include('products.urls', namespace="products")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


