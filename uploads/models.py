from django.db import models
from django.db.models.fields import Field
from .validators import validate_file_size
import uuid
import os
from django.conf import settings


def user_directory_path(instance, filename):
    global get_video_pk
    get_video_pk = instance.pk
    return f'videos/{filename}'


class Upload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.FileField(upload_to=user_directory_path, validators=[validate_file_size])

    def __str__(self):
        return f'{self.id}'

    def delete(self, *args, **kwargs):
        self.video.delete()
        os.removedirs(f'{settings.MEDIA_ROOT}videos/{self.id}')
        super().delete(*args, **kwargs)
