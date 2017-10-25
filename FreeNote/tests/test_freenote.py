# -*- coding: utf-8 -*-

import unittest
from django.test import Client
from pencil.models import User

class SimpleTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()

	def test_index(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_login(self):
		response = self.client.post('/accounts/login/', {'username': 'test', 'password': 'test1234'})
		self.assertEqual(response.status_code, 200)

	def test_logout(self):
		response = self.client.get('/accounts/logout/?next=/')
		self.assertEqual(response.status_code, 302)

# python manage.py test tests