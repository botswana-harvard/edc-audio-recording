from humanize import naturalsize

from django.conf import settings
from django.db import models
from django_crypto_fields.fields.encrypted_text_field import EncryptedTextField


def upload_folder():
    return str(settings.UPLOAD_FOLDER)


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

    def __str__(self):
        return 'Recording {}'.format(self.label)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.sound_filename.split('/')[-1:][0]
        self.report_datetime = self.start_datetime
        super(RecordingModelMixin, self).save(*args, **kwargs)

    def natural_key(self):
        return self.sound_filename

    def filesize(self):
        return naturalsize(self.sound_filesize, binary=True)

    class Meta:
        abstract = True
