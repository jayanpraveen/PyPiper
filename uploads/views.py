import os
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Upload
from django.conf import settings
from . import service
from .forms import Video_Form
from django.contrib import messages


def index(request):

    all_videos = Upload.objects.all()
    if request.method == 'POST':
        form = Video_Form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Video Uploaded")
            return HttpResponseRedirect(request.path)

    else:
        form = Video_Form()

    return render(request, 'uploads/index.html', {
        "form": form,
        "video": all_videos,
    })


def upload(request):
    return HttpResponse('<h1> -- upload -- </h1>')


def download(request):

    file_name = service.get_file_name()
    service.reduce_bitrate()

    path = f'completed/completed_{file_name}'
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/video/mp4')
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response

    return Http404
