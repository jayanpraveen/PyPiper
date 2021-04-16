import fnmatch
import os
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from .models import Upload
from django.conf import settings
from media.videos import convertor


def index(request):
    video = Upload.objects.all()
    form = Upload
    return render(request, 'uploads/index.html', {
        "form": form,
        "video": video
    })


def upload(request):
    return HttpResponse('<h1> -- upload -- </h1>')


def download(request):
    # input_name = os.listdir('media/videos')[0]
    for file in os.listdir('media/videos/.'):
        if fnmatch.fnmatch(file, '*.mp4'):
            input_name = file

    convertor.reduce_bitrate()

    path = f'completed/completed_{input_name}'
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(
                f.read(), content_type="application/video")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response
    return HttpResponse("<h1> -- 404 Not Found -- <h1>")
