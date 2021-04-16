from django.db import models


class Upload(models.Model):
    title = models.CharField(max_length=50)
    video = models.FileField(upload_to='videos')

    def __str__(self):
        return f'Caption/Title: {self.title}'
