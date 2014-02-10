from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError

import jsonfield

import logging
log = logging.getLogger(__name__)


class metadataModel(models.Model):
    """
    To hold user 'metadata' submissions
    """

    def save(self):
        """
        Override save to update timestamp
        """

        if self.finalized and self.finalizedTime is None:
            # Finalized is set, time was not set, we're finalizing this
            log.debug(" " * 5 + "Setting finalization TS")
            self.finalizedTime = datetime.now()
        elif self.finalizedTime:
            raise ValidationError(
                "Trying to save finalized Object:<id = %s>" %
                self.submissionID
            )
            # We have a finalize time and they're saving...

        self.modified = datetime.now()
        self.__syncForm()
        super(metadataModel, self).save()

    def __syncForm(self):
        """
        We do something not nice in this model, and have attributes
        that are in the JSON.  The model is the master, not the JSON
        """
        # Load
        #log.debug(self.mdForm)
        # Modify
        self.mdForm['META']['id'] = self.submissionID
        self.mdForm['META']['started'] = self.started.isoformat()
        self.mdForm['META']['last_modified'] = self.modified.isoformat()
        self.mdForm['META']['label'] = self.identifier
        self.mdForm['META']['finalized'] = self.finalized
        # Rewrite
        log.debug(self.mdForm)

    # In JSON
    submissionID = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=50, null=False, blank=False)

    # These two not in the JSON

    #   Also, this should be done by userid, not username... it's epscor
    #   generated id, but best we can do
    username = models.CharField(max_length=50, null=False, blank=False)
    #finished = models.BooleanField(default=False, null=False, blank=False)

    started = models.DateTimeField(null=False, blank=False,
            default=datetime.now)

    modified = models.DateTimeField(null=False, blank=False,
            default=datetime.now)

    # Set to make mostly immutable
    finalized = models.BooleanField(default=False, null=False, blank=False)

    # Do not manually edit this field.
    finalizedTime = models.DateTimeField(null=True, blank=True, default=None)

    # So -- most of these attributes are duplicated in the mdForm, but it would
    #  be handy to have the automagic django admin function.  We'll have to
    #  bind saves to the internals...

    mdForm = jsonfield.JSONField()
    # Some attributes will be overwritten automatically on save

    def finalize(self, *args, **kwargs):
        """
        So, to be really safe, I should use a proxy class, as this can be
        forced by setting finalized False, Nulling the time, and then saving...
        but that should never happen over the web UI
        """
        if self.finalized:
            raise Exception("Dataset already finalized!")
            # DIE!
        self.finalized = True
        self.save()
