from django.test import TestCase, Client
from django.urls import reverse
from uploads.models import *


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.url_index = reverse('media:index')
        # self.url_convert = reverse('media:convert')
        # self.url_download = reverse('media:download')

    def test_url_index_get(self):
        response = self.client.get(self.url_index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uploads/index.html')
