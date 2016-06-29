from django.db import models
from django.utils import timezone
import random


def interview_identifier():
    return ''.join([random.choice('ABCDEFGHKMNPRTUVWXYZ2346789') for _ in range(5)])


class InterviewManager(models.Manager):
    def get_by_natural_key(self, reference):
        return self.get(reference=reference)


class SubjectManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Subject(models.Model):

    name = models.CharField(max_length=15, unique=True)

    objects = SubjectManager()

    def natural_key(self):
        return (self.name, )

    class Meta:
        app_label = 'example'


class Interview(models.Model):

    subject = models.ForeignKey(Subject)

    report_datetime = models.DateTimeField(
        null=True,
        editable=False)

    reference = models.CharField(
        max_length=7,
        default=interview_identifier,
        unique=True)

    interview_datetime = models.DateTimeField(default=timezone.now)

    location = models.TextField(
        verbose_name='Where is this interview being conducted?',
        max_length=100,
    )

    interviewed = models.BooleanField(default=False, editable=False)

    objects = InterviewManager()

    def save(self, *args, **kwargs):
        self.report_datetime = self.interview_datetime
        super(Interview, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.reference, )
    natural_key.dependencies = ['example.subject']

    class Meta:
        app_label = 'example'
