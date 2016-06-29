import factory

from django.apps import apps as django_apps
from django.utils import timezone
from datetime import timedelta
from example.models import Interview, Subject
from django.test.testcases import TestCase


class TestSerialization(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name='ERIK')

    def interview(self):
        interview = Interview.objects.create(
            subject=self.subject,
            location='here')
