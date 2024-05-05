from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn('Invalid logout request', response.content.decode())

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'my_user_test', 'password': 'my_pass_test'},
            follow=True
        )
        print(response.content.decode())

        self.assertIn('This account is not logged', response.content.decode())

    def test_username_are_not_must_be_equal_request_username(self):
        user = User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        data = {'username': 'test_username', 'password': user.password}

        self.client.post(
            reverse('authors:logout'),
            data=data
        )

        self.assertNotEqual(user.username, data['username'])

    def test_logout_is_successfully(self):
        user = User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': user.username, 'password': user.password},
            follow=True
        )
        print(response.content.decode())

        self.assertIn('You are logout', response.content.decode())
