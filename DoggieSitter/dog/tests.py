import django.forms
from django.test import TestCase, tag, Client
from django.contrib.auth.models import User
from accounts.models import Accounts
import re
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from dog.models import Dog


# Create your tests here.


class DogView(TestCase):
    @tag('Hackaton')
    def test_AddDog_GET(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        response = self.client.get(reverse('dog:Adding', kwargs={'user_id': self.user.id}), follow=True)
        self.assertEqual(response.context['ok?'], 'yes!')

    @tag('Hackaton')
    def test_AddDog_POST_VALID(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        newform = {
            'name': 'test',
            'age': '2',
            'gender': 'male',
            'race': 'pizzi',
            'size': 'small',
            'hobby': 'love to test',
            'med': 'dsfsdcx'
        }
        response = self.client.post(reverse('dog:Adding', kwargs={'user_id': self.user.id}), data=newform, follow=True)
        self.assertEqual(response.context['ok?'], 'form is valid!')

    @tag('Hackaton')
    def test_AddDog_POST_NOT_VALID(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        newform = {
            'name': 'test',
            'age': 'dssds',
            'gender': 'male',
            'race': 'pizzi',
            'size': 'small',
            'hobby': 'love to test',
            'med': 'dsfsdcx'
        }
        response = self.client.post(reverse('dog:Adding', kwargs={'user_id': self.user.id}), data=newform, follow=True)
        self.assertEqual(response.context['ok?'], 'form is not valid!')

