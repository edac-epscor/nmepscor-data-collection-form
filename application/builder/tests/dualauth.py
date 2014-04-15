#from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase
from django.db import IntegrityError

import mock
from json import dumps

from builder.backends import RemoteDrupalBackend, DualAuthBackend


class fakeResponse(object):
    def __init__(self, text):
        self.text = text


def fakeRemoteAuth_good(**kwargs):
    return True, fakeResponse('<html><title>alice doe|junk</title></html>')


def fakeRemoteAuth_bad(**kwargs):
    return False, fakeResponse('<html><title>eve doe|junk</title></html>')


class BackendTest(TestCase):

    fixtures = ['dualauth-users.xml']
    backend = 'builder.backends.DualAuthBackend'

    @mock.patch("builder.util.remoteAuthenticate", fakeRemoteAuth_bad)
    def testAdminCascade(self):
        """
        This remote user should not exist, local should
        """

        kwargs = {
            'username': 'super',
            'password': 'secret'
        }

        # The remote user does not exist
        drupalUser = RemoteDrupalBackend().authenticate(**kwargs)
        self.assertIsNone(drupalUser)

        # The same local user does exist
        #self.client.login(**kwargs)
        modelUser = DualAuthBackend().authenticate(**kwargs)
        self.assertIsNotNone(modelUser)

        # Super user logged in.
        self.assertEqual(modelUser.is_superuser, True)

    @mock.patch("builder.util.remoteAuthenticate", fakeRemoteAuth_good)
    def testRemoteBackend(self):
        """
        This should create a new user if it doesn't exist
        """
        # Mock remote, go!

        num_users = User.objects.count()
        kwargs = {
            'username': 'alice',
            'password': 'secret'
        }
        drupalUser = RemoteDrupalBackend().authenticate(**kwargs)
        # They exist
        self.assertIsNotNone(drupalUser)

        # New user made
        self.assertEqual(User.objects.count(), num_users + 1)

    @mock.patch("builder.util.remoteAuthenticate", fakeRemoteAuth_bad)
    def testDualAuthBackend(self):
        """
        The admin user should be able to login and see normal pages
        """

        # More or less from django.contrib.auth.tests.context_processors

        self.client.login(username='super', password='secret')
        user = authenticate(username='super', password='secret')

        # User object with attributes
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'super')

    @mock.patch("builder.util.remoteAuthenticate", fakeRemoteAuth_bad)
    def testDualAuthFail(self):
        """
        The user is denied an  attempt to login with an invalid user.
        """

        num_users = User.objects.count()
        response = self.client.post('/signin',
            content_type='application/json',
            data=dumps({
                'username': 'baduser',
                'password': 'badpassword'
            })
        )

        self.assertEqual(response.status_code, 403)  # forbidden

        # No Change in user table
        self.assertEqual(User.objects.count(), num_users)

    @mock.patch("builder.util.remoteAuthenticate", fakeRemoteAuth_good)
    def testDoNotRecreate(self):
        """
        It should not create a user that already exists.
        """

        kwargs = {
            'username': 'super',
            'password': 'secret'
        }


        num_users = User.objects.count()

        try:
            drupalUser = RemoteDrupalBackend().authenticate(**kwargs)
        except IntegrityError:
            raise Exception("Attempting to create current user account")
