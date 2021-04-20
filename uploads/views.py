import os
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.shortcuts import render
from .models import Upload
from django.conf import settings
from . import service
from .forms import Video_Form
from django.contrib import messages


def index(request, key):
    if request.method == 'POST':
        form = Video_Form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Video Uploaded")
            return HttpResponseRedirect(f'/convert/{key}')

    else:
        form = Video_Form()

    formats = {
        "v2a": 'MP4 to MP3',
        "reduce_video": 'Compress video'
    }

    return render(request, 'uploads/index.html', {
        "form": form,
        "format": formats
    })


def convert(request,  key):

    print('\n\n\n==========     KEY    ================ =>', key, "\n\n\n")
    file_info = service.get_file_info()

    file_path = None
    if key == 'v2a':
        file_path = service.video_to_audio()
    if key == 'reduce_video':
        file_path = service.reduce_bitrate()

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=file_info.MIME)
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response

    return Http404
