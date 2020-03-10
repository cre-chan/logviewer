from django.urls import path
from . import views


app_name = 'logreader'
urlpatterns = [
    path('',views.search,name="search"),
    path('logs',views.logs,name="logs")
]
