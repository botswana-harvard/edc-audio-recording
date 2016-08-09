import json
import numpy as np
import sounddevice as sd

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView


class PlaybackView(TemplateView):

    template_name = 'edc_audio_recording/play.html'

    def __init__(self):
        # self.filename = None
        self.model_instance = None

    def get_context_data(self, **kwargs):
        context = super(PlaybackView, self).get_context_data(**kwargs)
        model = django_apps.get_model(self.kwargs.get('app_label'), self.kwargs.get('model_name'))
        self.model_instance = model.objects.get(pk=self.kwargs.get('pk'))
        context.update(
            is_popup=True,
            name=self.model_instance.label,
            verbose_name=self.model_instance._meta.verbose_name,
            pk=self.kwargs.get('pk'),
            # filename=self.filename,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlaybackView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            if request.GET.get('action') == 'play':
                soundfile = self.model_instance.sound_filename
                print(soundfile)
                data = np.load(soundfile).items()[0][1]
                sd.play(data, blocking=True)
                self.model_instance.played = True
                self.model_instance.save(update_fields=['played', 'modified'])
                response_data = {'status': str(sd.get_status()), 'status_code': 200}
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            elif request.GET.get('action') == 'stop':
                sd.stop()
                response_data = {'status': str(sd.get_status()), 'status_code': 200}
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                response_data = {'status': '', 'status_code': 200}
                return HttpResponse(json.dumps(response_data), content_type='application/json')
        return self.render_to_response(context)
