from .models import Upload
from django import forms


class Video_Form(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ("title", "video")
