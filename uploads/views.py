import os
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Upload
from . import service
from .forms import Video_Form
from uploads import models


def index(request):

    if request.method == 'POST':
        video_file = request.FILES['video']

        form = Video_Form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # print(f"\n\n\n{Upload.objects.all().first()}\n\n\n")

            key = Upload.objects.get(pk=models.get_video_pk)
            return HttpResponseRedirect(f'/{key}/')

    else:
        form = Video_Form()

    formats = {
        "v2a": 'mp4 to mp3',
        "reduce_video": 'Compress video'
    }

    return render(request, 'uploads/index.html', {
        "form": form,
        # "video":
        "format": formats
    })


def convert(request, key):
    service.get_key(key)
    service.reduce_bitrate()

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
