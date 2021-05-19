import os
import ffmpeg
from .models import Upload
from django.conf import settings
from collections import namedtuple
import mimetypes


def get_key(key):
    global pk
    pk = key


def get_file_info():
    uid = Upload.objects.get(id=pk)

    path = uid.video.path
    file = os.path.basename(path)
    file_name, file_ext = os.path.splitext(path)
    file_name = os.path.basename(file_name)
    file_mime = mimetypes.guess_type(path)[0]

    input_file_path = os.path.join(settings.MEDIA_ROOT, "videos", file)
    output_file_path = os.path.join(settings.MEDIA_ROOT, "completed", file_name)

    file_info = namedtuple(
        'file_info', ['name', 'ext', 'input_file', 'MIME', 'uid', 'output_path', 'input_path'])
    return file_info(
        file_name, file_ext, file, file_mime, uid, output_file_path, input_file_path)


def video_to_audio():
    media = get_file_info()
    proc = ffmpeg.input(media.input_path).audio
    proc = proc.output(f'{media.output_path}.mp3', audio_bitrate='320k')
    proc.run(overwrite_output=True)

    return None


def reduce_video(preset):
    media = get_file_info()
    proc = ffmpeg.input(media.input_path)
    proc = proc.output(
        f'{media.output_path}.mp4', crf=30, vcodec='libx264', acodec='copy', preset=preset)
    proc.run(overwrite_output=True)

    return None
