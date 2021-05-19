from os import name
from django.conf.urls import url
from django.urls import path
from . import views

app_name = "media"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:format>/<str:preset>/<uuid:key>/', views.convert, name='convert'),
    path('<str:format>/<uuid:key>/download/', views.download, name='download'),
]
