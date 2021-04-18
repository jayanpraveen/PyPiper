from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    print('file size ======>', filesize)
    if filesize > 55000000:
        raise ValidationError("Uploaded file must be less than 55 MB, Try again")
