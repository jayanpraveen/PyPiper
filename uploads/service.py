import os
import ffmpeg
from .models import Upload
from django.conf import settings
from collections import namedtuple
import subprocess
import mimetypes
import glob
import shutil


# # this deletes the input file
# def delete_input_video():
#     pk = get_file_info().uid
#     Upload.objects.get(id=pk).delete()


def get_key(key):
    global pk
    pk = key


def get_file_info():
    uid = str(Upload.objects.get(id=pk))

    path = glob.glob(f'media/videos/{uid}/*')[0]
    file = os.path.basename(path)
    file_name, file_ext = os.path.splitext(path)
    file_name = os.path.basename(file_name)
    file_mime = mimetypes.guess_type(path)[0]

    output_file_path = os.path.join(settings.MEDIA_ROOT, "completed", file_name)

    file_info = namedtuple('file_info', ['name', 'ext', 'in_file', 'MIME', 'uid', 'file_path'])
    return file_info(file_name, file_ext, file, file_mime, uid, output_file_path)


def video_to_audio():
    media = get_file_info()
    file = media.name + '.mp3'

    input_file = os.path.join(settings.MEDIA_ROOT, "videos", f'{media.uid}', media.in_file)
    output_file = os.path.join(settings.MEDIA_ROOT, "completed", file)

    proc = ffmpeg.input(input_file).audio
    proc = proc.output(output_file, audio_bitrate='320k')
    proc.run(overwrite_output=True)

    return output_file


def reduce_video():
    media = get_file_info()
    file = media.in_file

    input_file = os.path.join(settings.MEDIA_ROOT, "videos", f'{media.uid}', media.in_file)
    output_file = os.path.join(settings.MEDIA_ROOT, "completed", file)

    proc = ffmpeg.input(input_file)
    proc = proc.output(output_file, crf=32, preset='faster', vcodec='libx264', acodec='copy')
    proc.run(overwrite_output=True)

    return output_file
