import sys
import sounddevice as sd

from django.apps import AppConfig
from django.core.management.color import color_style


class AudioRecordingAppConfig(AppConfig):
    name = 'edc_audio_recording'
    verbose_name = 'Audio Recordings'

    def ready(self):
        style = color_style()
        try:
            sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
            device = sd.query_devices(None, 'input')
            sys.stdout.write(' * found audio input device \'{}\''.format(device['name']) + '\n')
        except (sd.PortAudioError, ValueError) as e:
            sys.stdout.write(
                style.WARNING(
                    'Warning: no compatible audio input devices found. '
                    'Audio recording will be disabled. Got {}\n'.format(str(e))))
