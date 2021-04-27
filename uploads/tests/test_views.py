from unittest import mock

from django.core import files
from uploads.forms import Video_Form
from django.core.files import File
from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from uploads.models import *
import uuid
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.format = 'v2a'
        self.key = uuid.uuid4()

        Upload.objects.create(id=self.key, video=f'{self.key}/video.mp4')

        self.url_index = reverse('media:index')
        self.url_convert = reverse('media:convert', args=[self.format, self.key])

    def test_url_index_get(self):
        """Result: Index page could not be loaded properly"""
        response = self.client.get(self.url_index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uploads/index.html')

    def test_url_convert_get_not_found(self):
        url_invalid_id = reverse('media:convert', args=['v2a', uuid.uuid4()])
        response = self.client.get(url_invalid_id)
        self.assertEquals(response.status_code, 404)

        url_invalid_id = reverse('media:convert', args=['reduce_video', uuid.uuid4()])
        response = self.client.get(url_invalid_id)
        self.assertEquals(response.status_code, 404)

    def test_url_download_get_not_found(self):
        url_invalid_id = reverse('media:download', args=['v2a', uuid.uuid4()])
        response = self.client.get(url_invalid_id)
        self.assertEquals(response.status_code, 404)

    def test_url_index_post(self):
        """Result: post Index page could not be loaded properly"""
        ui = uuid.uuid4()
        Upload.objects.create(
            id=ui,
            video=f'videos/{ui}/video.mp4'
        )

        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'video.mp4'
        self.file_model = Upload(video=self.file_mock)

        loaded_file = BytesIO(b"some dummy bcode data: \x00\x01")
        loaded_file.name = 'vid.mp4'

        response = self.client.post(self.url_index, files={
            'video': loaded_file
        })

        print(response.FILES)
        self.assertEqual(response.status_code, 200)
