import model_choices

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User

import logging
log = logging.getLogger(__name__)


# Create your models here.

class InvestigatorProfile(models.Model):
    LABEL = "Supervisor's "
    name = models.CharField(
        verbose_name=LABEL + "Name",
        max_length=50,
        blank=False,
        null=False,
    )

    institution = models.CharField(
        verbose_name=LABEL + "Institution",
        choices=model_choices.INSTITUTIONS,
        max_length=50,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        verbose_name=LABEL + "EMail",
        blank=False,
        null=False,
    )

    component = models.CharField(
        verbose_name="NM EPSCoR Component",
        choices=model_choices.COMPONENTS,
        max_length=25,
        blank=False,
        null=False,
    )

    class Meta:
        # One PI per email per user
        unique_together = ('email', 'name')

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
            'id': self.id,
            'name': self.name,
            'institution': self.institution,
            'email': self.email,
            'component': self.component,
        }


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True
    )
    # has last_login, email already

    component = models.CharField(
        verbose_name="NM EPSCoR Component",
        choices=model_choices.COMPONENTS,
        max_length=25,
        blank=False,
        null=False,
        default=model_choices.COMPONENTS[0]
    )

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
                'component': self.component,
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
        self.component = js['component']
        user.save()

        for investigator in js['investigators']:
            self.__jsonInvestigatorSave(
                investigator
            )
        self.save()

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
        updatedPI.component = investigator['component']
        updatedPI.save()


#  Hook user creation to build a profile object
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)
