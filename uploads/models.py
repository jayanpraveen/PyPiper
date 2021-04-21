from django.db import models
from django.db.models.fields import Field
from .validators import validate_file_size
import uuid
import os
import base64


def get_ui():
    return get_video_pk


def user_directory_path(instance, filename):
    global get_video_pk
    get_video_pk = instance.pk
    return f'videos/{instance.id}/{filename}'


class Upload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    video = models.FileField(upload_to=user_directory_path, validators=[validate_file_size])

    def __str__(self):
        return f'{self.id}'
        # return os.path.basename(self.video.name)
