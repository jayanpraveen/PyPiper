from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Upload


def index(request):
    video = Upload.objects.all()
    form = Upload
    return render(request, 'uploads/index.html', {
        "form": form,
        "video": video
    })
