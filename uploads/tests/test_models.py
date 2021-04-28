from unittest import mock
from unittest.mock import patch
from django.db import models
from django.test import TestCase
from uploads.models import *
from django.core.files import File
import uuid


class TestModelUpload(TestCase):
    def setUp(self):
        self.key = '2fce3dcc-f4aa-4bde-9217-b30268b048c2'
        Upload.objects.create(id=self.key, video=f'videos/{self.key}/f4aa_video.mp4')
        self.id = str(Upload.objects.all().first())

    def test_dunder_str(self):
        """testing for dunder str"""
        self.assertEqual(self.id, str(self.key))

    @patch('delete.os.removedirs')
    def test_delete(self, mocked_remove):
        """Error in deleting output directory"""
        Upload.objects.get(id=self.id).delete()
        self.assertTrue(mocked_remove.called)

    def test_function_upload_dir(self):
        """testing for upload dir"""
        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'video.mp4'
        self.file_model = Upload(video=self.file_mock)
        id = self.file_model.id
        video_name = str(id).split('-')[1] + '_' + 'video.mp4'
        self.assertEqual(user_directory_path(self.file_model, 'video.mp4'),
                         f'videos/{id}/{video_name}')
