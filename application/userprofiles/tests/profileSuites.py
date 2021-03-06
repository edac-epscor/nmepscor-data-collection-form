#from django.conf import settings
from django.test import TestCase

import mock
from json import loads, dumps

ALICE = {
    'username': 'alice1',
    'password': 'willbeaccepted'
}


def aliceDoes():
    return {
        u'email': u'alice@example.com',
        u'first': u'hello',
        u'last': u'world',
        u'component': u'SOLAR',  # Alice has a main component
        u'investigators': [{
            u'email': u'alice_boss@example.com',
            u'id': None,
            u'institution': u'UNM',
            u'component': u'SOLAR',
            u'name': u'New Investigator' #So does her boss
        }],
        u'username': u'alice1'
    }


def clientLogin(client, username='super', password='secret'):
    """
    Log in test client with our default fixture

    default args good for fixture
    """

    return client.login(
        username=username,
        password=password
    )


class fakeResponse(object):
    def __init__(self, text):
        self.text = text


def fakeRemoteAuth_good(**kwargs):
    return True, fakeResponse('<html><title>alice doe|junk</title></html>')


def fakeRemoteAuth_bad(**kwargs):
    return False, fakeResponse('<html><title>eve doe|junk</title></html>')


class ListInstitutionTest(TestCase):
    """
    Verify institution list works publicly
    """

    def testMembers(self):

        response = self.client.get('/users/institutions/list')
        institutions = loads(response.content)

        self.assertIn(
            ["UNM", "University of New Mexico"],
            institutions
        )


class ProfileEditing(TestCase):
    fixtures = ['profilesuite-users.xml']

    @mock.patch("builder.util.remoteAuthenticate", fakeRemoteAuth_good)
    def setUp(self):
        """ Alice is a newly created remote drupal user... """
        clientLogin(
            self.client,
            **ALICE
        )

        # With a good session
        session = self.client.session
        session['authenticated'] = True
        session.save()

    def testRead(self):

        response = self.client.get('/users/read')
        profile = loads(response.content)['profile']

        self.assertEqual(profile['username'], 'alice1')
        self.assertEqual(profile['first'], 'alice')

    def testUpdateMyName(self):
        """ Alice changes her name"""

        response = self.client.post('/users/update',
            content_type='application/json',
            data=dumps(aliceDoes())
        )

        # get back...ids in investigators new names
        profile = loads(response.content)['profile']
        self.assertEqual(profile['first'], 'hello')
        self.assertEqual(profile['last'], 'world')

    def testAddPI(self):
        """ Alice adds her PI"""
        response = self.client.post('/users/update',
            content_type='application/json',
            data=dumps(aliceDoes())
        )
        profile = loads(response.content)['profile']

         # new id assigned
        self.assertEqual(profile['investigators'][0]['id'], 1)

        self.assertEqual(
            profile['investigators'][0]['email'],
            'alice_boss@example.com'
        )

        # get back...ids in investigators new names

    def testDeletePI(self):
        """ Alice changes PIs """
        # Boss created
        self.client.post('/users/update',
            content_type='application/json',
            data=dumps(aliceDoes())
        )

        # Boss deleted
        response = self.client.post('/users/pis/delete',
            content_type='application/json',
            data=dumps({'pid': 1})
        )

        self.assertEqual(response.status_code, 200)

        # Boss does not show up any more
        response = self.client.get('/users/read')
        profile = loads(response.content)['profile']

        self.assertEqual(profile['investigators'], [])
