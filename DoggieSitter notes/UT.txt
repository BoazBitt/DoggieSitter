import django.db.models
from django.test import TestCase, tag , Client
import  json
from django.contrib.auth.models import User
from . import models , views, admin,forms
import re
import datetime
from accounts.models import Accounts ,PostTerms
from django import forms
from django.urls import reverse
from django.http import HttpRequest,HttpResponse


class BasicTests(TestCase):
    @tag('Unit-Test')
    def test_firstname(self):
        acc = models.Accounts()
        acc.first_name = 'Moran'
        self.assertTrue(len(acc.id) <= 9, 'Check name is less than 50 digits long')
        self.assertFalse(len(acc.id) > 50, 'Check name is less than 50 digits long')

    @tag('Unit-Test')
    def test_lastname(self):
        acc = models.Accounts()
        acc.last_name = 'Shalvi'
        self.assertFalse(len(acc.id) > 50, 'Check name is less than 50 digits long')

    @tag('Unit-Test')
    def test_id(self):
        acc = models.Accounts()
        acc.id = '123456789'
        self.assertTrue(len(acc.id) == 9, 'Check ID is 9 digits long')

    @tag('Unit-Test')
    def test_email(self):
        acc = models.Accounts()
        acc.email = 'Nadavg@mail.com'
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.assertTrue(re.fullmatch(regex, acc.email), 'check email format is valid')
        acc.email = 'Nadavgmail.com'
        self.assertFalse(re.fullmatch(regex, acc.email), 'check email format is valid')

    @tag('Unit-Test')
    def test_gender(self):
        genders = ['male', 'female']
        acc = models.Accounts()
        acc.gender = 'female'
        self.assertTrue(acc.gender in genders, ' gender test ')
        acc.gender = 'unknown'
        self.assertFalse(acc.gender in genders, 'gender test2')

    @tag('Unit-Test')
    def test_Date(self):
        acc = models.Accounts()
        acc.phone_number = '0526203790'
        self.assertEqual(acc.phone_number[0], '0', 'First digit is 0')
        self.assertEqual(acc.phone_number[1], '5', 'Second digit is 5')
        self.assertTrue(len(acc.phone_number) == 10, 'Check ID is 10 digits long1')
        acc.phone_number = '052620370'
        self.assertFalse(len(acc.phone_number) == 10, 'Check ID is 10 digits long2')

    @tag('Unit-Test')
    def test_address(self):
        acc = models.Accounts()
        acc.address = 'One Apple Park Way, Cupertino, CA 95014, United States'
        self.assertFalse(len(acc.address) <= 50, 'Check name is less than 50 digits long1')
        acc.address = 'One Apple Park Way, Cupertino, CA 95014, United States'
        self.assertTrue(len(acc.address) > 50, 'Check name is less than 50 digits long2')


class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.home = reverse('home')
        self.user = {
            'username': 'bobo',
            'password': '123456bo',
        }
        self.test = {
            'username': 'bobo',
            'password': '123456bo',
        }
        self.unmatching_user = {
            'username': 'username',
            'password': 'password',
        }
        self.user_unmatching_password = {
            'username': 'username',
            'password': 'teslatt',
        }
        return super().setUp()
    @tag('Unit-Test')
    def test_Logged(self):
        self.credentials = {
            'username': 'Boaz',
            'password': 'Bitton',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        login = self.client.login(username='Boaz', password='Bitton')
        self.assertTrue(login)



class InsertInfoTest(BaseTest):
    @tag('Integration-test')
    def test_can_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    @tag('Integration-test')
    def test_password_incorrect(self):
        response = self.client.post(self.login_url, self.user_unmatching_password, format='text/html')
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.status_code, 200)

    @tag('Integration-test')
    def test_user_incorrect(self):
        response = self.client.post(self.login_url, self.unmatching_user, format='text/html')
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.status_code, 200)


class LogInTest(TestCase):
    @tag('Unit-Test')
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': '5t4r3e2w1q',
        }
        user = User.objects.create_user(**self.credentials)
        user.is_active = True

    @tag('Unit-Test')
    def test_login(self):
        response = self.client.post('/accounts/login/', **self.credentials, follow=True)
        status = response.context['user'].is_active
        self.assertFalse(status)

    @tag('Unit-Test')
    def test_logout(self):
        response = self.client.post('/accounts/login/', **self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)


class DeleteUser(TestCase):
    @tag('Unit-Test')
    def test_delete(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'user@gmail.com',
            'password': 'userpassdskfldskf'
        }
        user = User.objects.create_user(**self.credentials)
        us = User.objects.get(username=user)
        us.delete()
        self.assertFalse(User.objects.filter(username=us).exists())

class CreateTypeUser(TestCase):
    @tag('Unit-Test')
    def test_create_Doggie_approved(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        acc = models.Accounts(user)
        acc.is_doggiesitter = True
        acc.approved = True
        isDoggie = acc.is_doggiesitter
        isApproved = acc.approved
        self.assertTrue(isDoggie)
        self.assertFalse(not isApproved)

    @tag('Unit-Test')
    def test_create_Doggie_not_approved(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        acc = models.Accounts(user)
        acc.is_doggiesitter = True
        acc.approved = False
        isDoggie = acc.is_doggiesitter
        isApproved = acc.approved
        self.assertTrue(isDoggie)
        self.assertFalse(isApproved)

    @tag('Unit-Test')
    def test_create_Owner(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        acc = models.Accounts(user)
        acc.is_doggiesitter = False
        isDoggie = acc.is_doggiesitter
        self.assertFalse(isDoggie)

class EditUser(TestCase):
    @tag('Unit-Test')
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }

    @tag('Unit-Test')
    def test_Changeinfo_Username(self):
        user = User.objects.create_user(**self.credentials)
        us = User.objects.filter(pk=user.id).first()
        us.username = 'newname'
        self.assertNotEqual(us.username, 'testuser')

    @tag('Unit-Test')
    def test_Changeinfo_password(self):
        user = User.objects.create_user(**self.credentials)
        us = User.objects.filter(pk=user.id).first()
        us.set_password('pass')
        self.assertNotEqual(us.password, 'testuser')

    @tag('Unit-Test')
    def test_Changeinfo_First_Name(self):
        user = User.objects.create_user(**self.credentials)
        us = User.objects.filter(pk=user.id).first()
        us.first_name = 'newname'
        self.assertNotEqual(us.username, 'test')

    @tag('Unit-Test')
    def test_Changeinfo_Last_Name(self):
        user = User.objects.create_user(**self.credentials)
        us = User.objects.filter(pk=user.id).first()
        us.last_name = 'newname'
        self.assertNotEqual(us.username, 'unit')


class Integrate_tests(TestCase):
    @tag('Integration-test')
    def test_Log_in_out(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpass'
        }
        user = User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='userpass')
        self.assertTrue(login)
        logout = self.client.logout()
        self.assertTrue(user.is_active)

    @tag('Integration-test')
    def test_create_delete(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user1 = User.objects.create_user(**self.credentials)

        self.credentials = {
            'username': 'testuser2',
            'password': 'userpassdskfldskf',
            'first_name': 'test2',
            'last_name': 'unit2',
        }
        user2 = User.objects.create_user(**self.credentials)

        self.credentials = {
            'username': 'testuser3',
            'password': 'userpassdskfldskf',
            'first_name': 'test3',
            'last_name': 'unit3',
        }
        user3 = User.objects.create_user(**self.credentials)

        for i in User.objects.all():

            if i.username == user3.username:
                i.username = 'Newname'
                user2.username = 'testuser3'
                self.assertNotEqual(i.username, user2.username)

class View_test(TestCase):
    @tag('Unit-Test')
    def test_about_GET(self):
        client = Client()
        response = client.get(reverse('about'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'about.html')

    @tag('Unit-Test')
    def test_gallery_GET(self):
        client = Client()
        response = client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery.html')

    @tag('Unit-Test')
    def test_user_info_GET(self):
        client = Client()
        response = client.get(reverse('user_info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_info.html')

    @tag('Unit-Test')
    def test_SearchUserByID(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        request = HttpRequest()
        request.POST.appendlist('username', user.username)
        response = views.SearchUserByID(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_GetAccounts(self):
        request = HttpRequest()
        response = views.GetAccounts(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_password_success(self):
        request = HttpRequest()
        response = views.password_success(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_SignUpView_GET(self):
        request = HttpRequest()
        response = views.SignUpView(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_SignUpView_POST_notValid(self):
        request = HttpRequest()
        request.method = 'POST'
        response = views.SignUpView(request)
        self.assertEqual(response.status_code,200)
    @tag('Unit-Test')
    def test_SignUpView_POST_Valid(self):
        date_of_birth =datetime.datetime(2007,7,5)
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'username': 'Boaz',
            'password1': '123456Bb',
            'password2': '123456Bb',
            'first_name':'bo',
            'last_name': 'az',
            'gender': 'male',
            'date_of_birth':'January 15 2000',
            'id': '123456789',
            'email': 'Bo@gmail.com',
            'phone_number' : '1234567890',
            'address':'Bobo street',
            'is_doggiesitter': False
        }
        response = self.client.post(reverse('signup'), request.POST, follow=True)
        self.assertEqual(response.status_code,200)
        # self.assertTemplateUsed(response,'home.html')

    @tag('Unit-Test')
    def test_SearchUserByID_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {'search_id': ''}
        response = views.SearchUserByID(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_SearchUserByID_POSTLen(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',

        }
        self.user = User.objects.create_user(**self.credentials)
        self.acc = Accounts.objects.create(user=self.user, is_doggiesitter=False, id='1')
        self.user.save()
        self.acc.save()
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {'search_id': self.user.id}
        test = Accounts.objects.filter(id=request.POST.get("search_id"))
        response = views.SearchUserByID(request)
        self.assertEqual(response.status_code, 200)

    @tag('Unit-Test')
    def test_GetUsername_POST(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        request = HttpRequest()
        response = views.GetUsername(request,user.username)
        self.assertEqual(response.status_code,200)
    @tag('Unit-Test')
    def test_go_home(self):
        request = HttpRequest()
        response = views.go_home(request,'home.html')
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_Terms_GET(self):
        request = HttpRequest()
        request.method = 'GET'
        response = views.Terms(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_ChangePassword_correct(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        request = HttpRequest()
        request.POST = {'user_n': user.username ,'new_pass1': '123456Bb', 'new_pass2': '123456Bb'}
        response = views.ChangePassword(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_ChangePassword_notEqual(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        request = HttpRequest()
        request.POST = {'user_n': user.username, 'new_pass1': '123456Bb', 'new_pass2': '123456'}
        response = views.ChangePassword(request)
        self.assertEqual(response.status_code, 200)

    @tag('Unit-Test')
    def test_ChangePassword_notValid(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        request = HttpRequest()
        request.POST = {'user_n': user.username, 'new_pass1': '123', 'new_pass2': '123'}
        response = views.ChangePassword(request)
        self.assertEqual(response.status_code, 200)

    @tag('Unit-Test')
    def test_Term_Except(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'title_name': 1,
            'body_name' : 'Bitton',
            'author_name': 'Was here'
        }
        response = views.Terms(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_Changeinfo_GET(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        self.acc = Accounts.objects.create(user=self.user,is_doggiesitter = False)
        self.user.save()
        self.acc.save()
        response = self.client.get(reverse('changeinfo', kwargs={'user_id':self.user.id}),data='',follow=True)
        self.assertEqual(response.context['ok?'], 'yes!')

    @tag('Unit-Test')
    def test_Changeinfo_POST_valid(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        self.acc = Accounts.objects.create(user=self.user, is_doggiesitter=False)
        self.user.save()
        self.acc.save()
        newform = {'first_name': 'Boaz', 'last_name': 'Bitton ', 'email': 'B@gmail.com', 'phone_number': '1234567890'}
        response = self.client.post(reverse('changeinfo', kwargs={'user_id': self.user.id}), data=newform, follow=True)
        self.assertEqual(response.context['ok?'], 'form is valid!')

    @tag('Unit-Test')
    def test_Changeinfo_POST_notvalid(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        self.acc = Accounts.objects.create(user=self.user, is_doggiesitter=False)
        self.user.save()
        self.acc.save()
        newform = {'first_name': 'Boaz', 'last_name': 'Bitton ', 'email': 'Bgmail', 'phone_number': '1234567890'}
        response = self.client.post(reverse('changeinfo', kwargs={'user_id': self.user.id}), data=newform, follow=True)
        self.assertEqual(response.context['ok?'], 'form is not valid!')



# class Form_test(TestCase):
#     @tag('x')
#     def test_clean_email(self):
#         t = forms.ModelForm()
#         acc = forms.AccountChangeForm(t)
#         acc.cleaned_data['email'] = 'test@gmail.com'
#         response = forms.AccountChangeForm.clean_email(acc)
#         print(response)


class Admin_test(TestCase):
    @tag('Unit-Test')
    def test_delete_user(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        user = User.objects.create_user(**self.credentials)
        request = HttpRequest()
        request.POST = {'selected_id': user.username}
        response = admin.delete_user(request)
        self.assertEqual(response.status_code,200)

    @tag('Unit-Test')
    def test_make_admin(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        self.acc = Accounts.objects.create(user=self.user,is_doggiesitter = False)
        self.user.save()
        self.acc.save()
        request = HttpRequest()
        form_data ={'selected_id': self.user.username}
        response = self.client.post(reverse('admin_actions/make_admin'),data=form_data, follow=True)
        self.assertEqual(response.context['result'], 'Admin permissions was successfully granted.')

    @tag('Unit-Test')
    def test_delete_admin(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        self.acc = Accounts.objects.create(user=self.user,is_doggiesitter = False)
        self.user.save()
        self.acc.save()
        request = HttpRequest()
        form_data = {'selected_id': self.user.username}
        response = self.client.post(reverse('admin_actions/remove_admin'), data=form_data, follow=True)
        self.assertEqual(response.context['result'], 'Admin permissions was successfully denied.')

    @tag('Unit-Test')
    def test_Approve_Doggie(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'userpassdskfldskf',
            'first_name': 'test',
            'last_name': 'unit',
        }
        self.user = User.objects.create_user(**self.credentials)
        self.acc = Accounts.objects.create(user=self.user,is_doggiesitter = True)
        self.user.save()
        self.acc.save()
        request = HttpRequest()
        form_data = {'selected_id': self.user.username}
        response = self.client.post(reverse('admin_actions/approve_doggiesitter'), data=form_data, follow=True)
        self.assertEqual(response.context['result'], 'Doggiesitter was successfully approved.')

