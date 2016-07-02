from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from edc_audio_recording.models import RecordingModelMixin, upload_folder


class HomeView(EdcBaseViewMixin, TemplateView):

    template_name = 'edc_audio_recording/home.html'

    def __init__(self, *args, **kwargs):
        self._recording_data = {}
        super(HomeView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            recording_data=self.recording_data
        )
        return context

    @property
    def recording_data(self):
        if not self._recording_data:
            for model in self.recording_models():
                self._recording_data.update({
                    model._meta.verbose_name: self.recordings_for_model(model)})
        return self._recording_data

    def create_wav_files(self, model):
        objects = model.objects.all().order_by('report_datetime', 'label')
        for obj in objects:
            obj.create_wav_file()
        return objects

    def recordings_for_model(self, model):
        objects = self.create_wav_files(model)
        recordings_for_model = dict(
            upload_folder=upload_folder,
            opts=model._meta,
            app_label=model._meta.app_label,
            model_name=model._meta.model_name,
            fk=model._meta.object_name.split('recording')[0],
            verbose_name=model._meta.verbose_name,
            objects=objects)
        return recordings_for_model

    def recording_models(self):
        recording_models = []
        for app in django_apps.get_app_configs():
            for model in app.get_models():
                if issubclass(model, RecordingModelMixin):
                    recording_models.append(model)
        return recording_models

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
