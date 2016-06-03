from django.db import models


class RecordingManager(models.Manager):

    def get_by_natural_key(self, sound_filename):
        return self.get(sound_filename=sound_filename)
