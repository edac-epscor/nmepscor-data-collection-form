import model_choices

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User

import logging
log = logging.getLogger(__name__)


# Create your models here.

class InvestigatorProfile(models.Model):
    name = models.CharField(
        verbose_name="Principle Investigator's Name",
        max_length=50,
        blank=False,
        null=False,
    )

    institution = models.CharField(
        verbose_name="Principle Investigator's Institution",
        choices=model_choices.INSTITUTIONS,
        max_length=50,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        verbose_name="Principle Investigator's EMail",
        blank=False,
        null=False,
        unique=True,  # One PI per email
    )

    # Reverse
    profile = models.ForeignKey(
        'UserProfile',
        related_name='investigators'
    )

    def __unicode__(self):
        return u"%(name)s (%(institution)s) <%(email)s>" % {
            'name': self.name,
            'institution': self.institution,
            'email': self.email,
        }

    def ajax(self):
        return {
            'InvestigatorProfile': {
                'id': self.id,
                'name': self.name,
                'institution': self.institution,
                'email': self.email,
            }
        }


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True
    )
    # has last_login, email already

    #investigators = models.ManyToManyField(InvestigatorProfile)

    def __unicode__(self):
        return u"Profile for <%s>" % self.user.username

    def ajax(self):
        user = self.user
        return {
            'profile': {
                'username': user.username,
                'first': user.first_name,
                'last': user.last_name,
                'email': user.email,
                'investigators': [i.ajax() for i in
                    self.investigators.select_related()]
            }
        }

    def jsonSave(self, js):
        # You can't do the user, but can do the name...
        user = self.user
        user.first_name = js['first']
        user.last_name = js['last']
        user.email = js['email']

        for investigator in js['investigators']:
            self.__jsonInvestigatorSave(
                investigator['InvestigatorProfile']
            )

    def __jsonInvestigatorSave(self, investigator):
        """
        InvestgiatorJSON
        """

        if investigator['id']:
            updatedPI = self.investigators.select_related().get(
                pk=investigator['id']
            )
        else:
            updatedPI = self.investigators.create()

        updatedPI.name = investigator['name']
        updatedPI.institution = investigator['institution']
        updatedPI.email = investigator['email']
        updatedPI.save()


#  Hook user creation to build a profile object
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)
