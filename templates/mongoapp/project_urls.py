# project/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mongoapp/', include('mongoapp.urls')),
    # Add more app URLs as needed
]
