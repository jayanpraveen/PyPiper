from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from uploads.models import Upload
import uuid


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.format = 'v2as'
        self.key = uuid.uuid4()

        Upload.objects.create(id=self.key, video=f'{self.key}/video.mp4')

        self.url_index = reverse('media:index')
        self.url_convert = reverse('media:convert', args=[self.format, self.key])

    def test_url_index_get(self):
        """Index page could not be loaded properly"""
        response = self.client.get(self.url_index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uploads/index.html')

    def test_url_convert_get_found(self):
        """Convert page could not be loaded"""
        response = self.client.get(self.url_convert, {
            'format': self.format,
            'key': self.key
        })
        self.assertEquals(response.status_code, 200)

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
