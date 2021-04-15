from django.db import models


class Upload(models.Model):
    title = models.CharField(max_length=50)
    video = models.FileField(upload_to='videos')
    url_64encoding = models.CharField(
        max_length=2048, default='/upload/videos/')

    def __str__(self):
        return f'Caption: {self.title}'
