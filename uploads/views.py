import os
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

    return render(request, 'uploads/index.html', {"form": form})


def convert(request, format, key):
    formats = ["reduce_video", "v2a"]
    if Upload.objects.filter(pk=key).exists() and format in formats:
        service.get_key(key)

        if format == 'reduce_video':
            service.reduce_video()

        if format == 'v2a':
            service.video_to_audio()

        return render(request, 'uploads/download.html', {'id': key, 'format': format})
    else:
        raise Http404


def download(request, format, key):

    path = f'videos/'
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        service.get_key(key)
        file_path = service.get_file_info().output_path
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
