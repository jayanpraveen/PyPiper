from django.core.exceptions import ValidationError


def validate_file_size(file):
    filesize = file.size
    if filesize > 30000000:
        raise ValidationError("Uploaded file must 30 MB or less, Try again!")
