from os import name
from django.conf.urls import url
from django.urls import path
from . import views

app_name = "media"
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:key>/', views.index, name='index'),
    path('convert/<slug:key>/', views.convert, name='convert'),

]
