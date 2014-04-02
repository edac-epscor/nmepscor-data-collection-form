from django.conf import settings
from django.contrib.auth.models import User, Group, Permission, AnonymousUser
from django.contrib.auth import authenticate
from django.test import TestCase


class BackendTest(TestCase):

    backend = 'nmepscor-data-collection-form.builder.backends.DualAuthBackend'
    #fixtures = ['dualAuthTestData.json']
    fixtures = ['dualauth-users.xml']

    def testLocalBack(self):
        """
        """
        pass

    def testAdminCascade(self):
        """
        """
        pass

    def testRemoteBackend(self):
        """
        Mock remote server, go
        """
        pass

    def dualAuthBackend(self):
        """
        More or less from django.contrib.auth.tests.context_processors

        The admin user should be able to login and see normal pages
        """

        self.client.login(username='super', password='secret')
        user = authenticate(username='super', password='secret')

        # User object with attributes
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'super')

        response = self.client.get('/auth_processor_user/')
        self.assertContains(response, "unicode: super")
        self.assertContains(response, "id: 100")
        self.assertContains(response, "username: super")

    def dualAuthFail(self):
        """
        The user should attempt to login with an invalid remote user.
        """
        num_users = User.objects.count()
        response = self.client.post('/signin', {
            'username': 'baduser',
            'password': 'badpassword'
        })

        self.assertEqual(response.status_code, 403)  # forbidden

        # No Change
        self.assertEqual(User.objects.count(), num_users)
