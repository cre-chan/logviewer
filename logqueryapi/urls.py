from django.urls import path
from . import views


app_name = 'logqueryapi'
urlpatterns = [
    path('',views.logs_generic,name="generic"),
]
