# mongoapp/urls.py
from django.urls import path
from .views import mongo_data_list

urlpatterns = [
    path('mongo-data-list/', mongo_data_list, name='mongo_data_list'),
    # Add more URLs as needed
]
