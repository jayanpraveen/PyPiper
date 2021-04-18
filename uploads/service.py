import os
import ffmpeg
from django.conf import settings
import glob
import subprocess
from .models import Upload


def get_file_name():
    file_name = glob.glob('media/videos/*.mp4')[0]
    file_name = os.path.basename(file_name).split('.')[0]
    return file_name + ".mp4"


def reduce_bitrate():
    file_name = None
    file_name = get_file_name()
    print(file_name)

    input_file = os.path.join(
        settings.MEDIA_ROOT, "videos", f'{file_name}')
    output_file = os.path.join(
        settings.MEDIA_ROOT, "completed", f'completed_{file_name}')

    video_bitrate = '1200k'

    (
        ffmpeg.input(input_file)
        .output(output_file, video_bitrate=video_bitrate)
        .run(overwrite_output=True)
    )

    remove_objects_table()
    remove_input_file(input_file)


def remove_objects_table():
    Upload.objects.all().delete()


def remove_input_file(input_file):
    print('Removing user input file...')
    os.remove(input_file)
