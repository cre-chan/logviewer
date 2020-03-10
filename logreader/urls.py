from django.urls import path
from .views import search,logs


app_name = 'logreader'
urlpatterns = [
    path('',search,name="search"),
    path('logs',logs,name="logs")
]
