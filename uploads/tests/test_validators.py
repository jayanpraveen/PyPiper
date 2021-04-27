from django.test import TestCase
from django.core.files import File
from unittest import mock

from uploads.models import Upload
from uploads.validators import *
from uploads.service import *
from django.core.exceptions import ValidationError


class TestValidators(TestCase):
    def setUp(self):
        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'video.mp4'

    def test_file_fiel(self):
        self.file_mock.size = 30000000
        file_model = Upload(video=self.file_mock)

        self.assertEqual(validate_file_size(file_model.video), None)

    def test_file_fiel_raise_error(self):
        self.file_mock.size = 90000000
        file_model = Upload(video=self.file_mock)

        with self.assertRaises(ValidationError):
            validate_file_size(file_model.video)
