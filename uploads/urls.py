from os import name
from django.conf.urls import url
from django.urls import path
from . import views

app_name = "media"
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name="upload"),
    path('download/', views.download, name="download"),
]
