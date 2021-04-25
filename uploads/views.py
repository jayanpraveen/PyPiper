import os
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
            return HttpResponseRedirect(f'{format}/{key}/')

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
    service.get_key(key)

    if format == 'reduce_video':
        service.reduce_bitrate()

    if format == 'v2a':
        service.video_to_audio()

    return render(request, 'uploads/convert.html', {'id': key})


def download(request, key):
    service.get_key(key)
    file_path = service.get_file_info().out
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=service.get_file_info().MIME)
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response
    return Http404
