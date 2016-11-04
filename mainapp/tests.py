from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.

class UserTestCase(TestCase):
	def setUp(self):
		u1 = User.objects.create_user('test1', 'a@a.com', '123456')
		u2 = User.objects.create_user('test2', 'b@b.com', '123456')
		u3 = User.objects.create_user('test3', 'c@c.com', '123456')

	def test_can_user_login(self):
		self.assertEqual(User.objects.filter(username = 'test1').exists(), True)
		self.assertEqual(User.objects.filter(username = 'test2').exists(), True)
		self.assertEqual(User.objects.filter(username = 'test3').exists(), True)