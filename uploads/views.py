import os
from os import path
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Upload
from . import service
from .forms import Video_Form
from uploads import models


def index(request):
    if request.method == 'POST':
        form = Video_Form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            key = Upload.objects.get(pk=models.get_video_pk)
            format = request.POST['formats']
            return HttpResponseRedirect(reverse('media:convert', kwargs={
                'format': format,
                'key': key
            }))

    else:
        form = Video_Form()

    formats = {
        "reduce_video": 'Compress video',
        "v2a": 'mp4 to mp3',
    }

    return render(request, 'uploads/index.html', {
        "form": form,
        "format": formats
    })


def convert(request, format, key):
    if Upload.objects.filter(pk=key).exists():
        service.get_key(key)

        if format == 'reduce_video':
            service.reduce_bitrate()

        if format == 'v2a':
            service.video_to_audio()

        return render(request, 'uploads/download.html', {'id': key, 'format': format})
    else:
        raise Http404


def download(request, format, key):

    path = f'videos/{key}'
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        # if os.path.exists(f''):
        service.get_key(key)
        file_path = service.get_file_info().file_path
        if format == 'reduce_video':
            file_path = file_path + ".mp4"
        if format == 'v2a':
            file_path = file_path + ".mp3"

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=service.get_file_info().MIME)
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response

    raise Http404
