import os
import ffmpeg
from django.conf import settings
import fnmatch

for file in os.listdir('media/videos/.'):
    if fnmatch.fnmatch(file, '*.mp4'):
        file_name = file


def reduce_bitrate():
    input_file = os.path.join(
        settings.MEDIA_ROOT, "videos", f'{file_name}')
    output_file = os.path.join(
        settings.MEDIA_ROOT, "completed", f'completed_{file_name}')
    video_bitrate = '500k'

    (
        ffmpeg.input(input_file)
        .output(output_file, video_bitrate=video_bitrate).run(overwrite_output=True)
    )
