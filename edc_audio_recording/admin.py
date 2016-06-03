from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from edc_base.modeladmin.mixins import ModelAdminChangelistModelButtonMixin


class RecordingAdminSite(AdminSite):
    site_header = 'Audio Recordings'
    site_title = 'Audio Recordings'
    index_title = 'Audio Recordings Admin'
    site_url = '/recording/'

recording_admin = RecordingAdminSite(name='recording_admin')


class ModelAdminAudioPlaybackMixin(object):

    def play(self, obj):
        kwargs = {'app_label': obj._meta.app_label, 'model_name': obj._meta.model_name, 'pk': obj.pk}
        url = reverse('play', kwargs=kwargs)
        return format_html(
            '<button id="play-{id}" onclick="return startPlayback(\'{id}\', \'{url}\');" '
            'class="button">Play</button>', id=obj.pk, url=url)
    play.short_description = 'Play'

    def stop(self, obj):
        kwargs = {'app_label': obj._meta.app_label, 'model_name': obj._meta.model_name, 'pk': obj.pk}
        url = reverse('play', kwargs=kwargs)
        return format_html(
            '<button id="stop-{id}" onclick="return stopPlayback(\'{id}\', \'{url}\');" '
            'class="button">Stop</button>', id=obj.pk, url=url)
    stop.short_description = 'Stop'

    def record(self, obj):
        kwargs = {'app_label': obj._meta.app_label, 'model_name': obj._meta.model_name, 'pk': obj.pk}
        url = reverse('record', kwargs=kwargs)
        return format_html(
            '<a id="record-{id}" href="{url}" '
            'class="button">Record</a>', id=obj.pk, url=url)
    record.short_description = 'record'


class ModelAdminRecordingMixin(ModelAdminAudioPlaybackMixin, ModelAdminChangelistModelButtonMixin):

    date_hierarchy = 'start_datetime'

    list_per_page = 5

    fields = [
        'label', 'verified', 'comment',
        'start_datetime', 'stop_datetime', 'sound_filename',
        'sound_filesize', 'recording_time']

    radio_fields = {'verified': admin.VERTICAL}

    list_display = ['label', 'play', 'stop', 'verified', 'played', 'recording_time', 'filesize',
                    'start_datetime', 'stop_datetime', ]

    list_filter = ['verified', 'played', 'start_datetime']

    search_fields = ['label', 'sound_filename']

    ordering = ('-start_datetime', )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(ModelAdminRecordingMixin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + [
            'label', 'start_datetime', 'stop_datetime', 'sound_filename',
            'sound_filesize', 'recording_time']
