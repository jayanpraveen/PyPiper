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
        self.key = '058ba73c-f897-4aca-938e-f84c119740e2'

        Upload.objects.create(id=self.key, video=f'videos/{self.key}/f897_video.mp4')

        self.url_index = reverse('media:index')
        self.url_convert = reverse('media:convert', args=[self.format, self.key])
        self.url_download = reverse('media:download', args=[self.format, self.key])

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

    # note: place a video of the same name in the respective dir
    def test_url_convert_get_found(self):
        """Convert page could not be loaded"""
        response = self.client.get(self.url_convert, {
            'format': self.format,
            'key': self.key
        })
        self.assertEquals(response.status_code, 200)

    def test_url_download_get_found(self):
        """Convert page could not be loaded"""
        response = self.client.get(self.url_download, {
            'format': self.format,
            'key': self.key
        })
        self.assertEquals(response.status_code, 200)
