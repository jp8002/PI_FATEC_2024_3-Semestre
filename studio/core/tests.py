from django.test import TestCase
from django.urls import reverse as r
# Create your tests here.

class testePaginaInicial(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('paginaInicial'))
        
    def test_200_response(self):
         self.assertEqual(self.resp.status_code,200)