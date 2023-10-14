
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path("contacts/", include('contacts.urls', namespace="contacts")),
    path("experts/", include('experts.urls', namespace="experts")),
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
    path("education/", include('education.urls', namespace="education")),
    path('tinymce/', include('tinymce.urls')), #add this
    path("trainings/", include('trainings.urls', namespace="trainings")),
    path("trainingapplications/", include('trainingapplications.urls', namespace="trainingapplications")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

