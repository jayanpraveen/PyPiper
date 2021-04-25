from os import name
from django.conf.urls import url
from django.urls import path
from . import views

app_name = "media"
urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:key>/download/', views.download, name='download'),
    path('<str:format>/<uuid:key>/', views.convert, name='convert'),
]
