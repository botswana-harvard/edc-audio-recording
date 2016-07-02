import os
import numpy as np
import soundfile as sf

from humanize import naturalsize

from django.conf import settings
from django.db import models
from django_crypto_fields.fields.encrypted_text_field import EncryptedTextField
from django.core.urlresolvers import reverse


def upload_folder():
    return str(settings.UPLOAD_FOLDER)


class RecordingManager(models.Manager):

    def get_by_natural_key(self, sound_filename):
        return self.get(sound_filename=sound_filename)


class RecordingModelMixin(models.Model):

    report_datetime = models.DateTimeField(
        null=True,
        editable=False)

    label = models.CharField(
        max_length=25,
        null=True,
        help_text=(
            'Friendly name for this recording or partial recording '
            'e.g. part 1, part2, or may be left blank.'))

    start_datetime = models.DateTimeField(null=True)

    stop_datetime = models.DateTimeField(null=True)

    recording_time = models.CharField(
        max_length=10,
        null=True)

    sound_file = models.FileField(
        upload_to=upload_folder,
        null=True)

    sound_filename = models.CharField(
        max_length=150,
        unique=True)

    sound_filesize = models.FloatField(
        default=0.0,
        blank=True)

    comment = EncryptedTextField(
        verbose_name="Additional comment that may assist in analysis of this discussion",
        max_length=250,
        blank=True,
        null=True
    )

    played = models.BooleanField(default=False, editable=False)

    objects = RecordingManager()

    def __str__(self):
        return 'Recording {}'.format(self.label)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.sound_filename.split('/')[-1:][0]
        self.report_datetime = self.start_datetime
        super(RecordingModelMixin, self).save(*args, **kwargs)

    def natural_key(self):
        return self.sound_filename

    def get_absolute_url(self):
        return reverse(
            'recording_admin:' + self._meta.app_label + '_' + self._meta.model_name + '_change',
            args=[str(self.id)])

    def filesize(self):
        return naturalsize(self.sound_filesize, binary=True)

    @property
    def file_exists(self):
        """Return true if file exists."""
        sound_file_exists = False
        if self.sound_filename:
            sound_file_exists = os.path.isfile(self.sound_file_current_path)
        return sound_file_exists

    @property
    def file_path(self):
        """Return current path based on this app's upload folder."""
        return os.path.join(upload_folder(), self.sound_filename.split('/')[-1:][0])

    @property
    def file_name(self):
        return self.sound_filename.split('/')[-1:][0]

    def create_wav_file(self):
        if not os.path.isfile(self.wav_file_path):
            if os.path.isfile(self.file_path):
                sf.write(self.wav_file_path, np.load(self.file_path)['arr_0'], samplerate=44100)

    @property
    def wav_file_path(self):
        """Return current path based on this app's upload folder."""
        return os.path.join(upload_folder(), self.wav_file_name)

    @property
    def wav_file_name(self):
        return self.file_name.split('.')[0] + '.wav'

    @property
    def wav_file_exists(self):
        """Return true if file exists."""
        return os.path.isfile(self.wav_file_path)

    class Meta:
        abstract = True
