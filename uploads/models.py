from django.db import models
from .validators import validate_file_size


class Upload(models.Model):
    title = models.CharField(max_length=50)
    video = models.FileField(
        upload_to='videos', validators=[validate_file_size])

    def __str__(self):
        return f'Title: {self.title}'
