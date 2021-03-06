import sys
import sounddevice as sd

from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style


class AppConfig(DjangoAppConfig):
    name = 'edc_audio_recording'
    verbose_name = 'Audio Recordings'
    audio_file_extensions = ['.npz']

    def ready(self):
        style = color_style()
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        try:
            device = sd.query_devices(None, 'input')
            sys.stdout.write(' * found audio input device \'{}\''.format(device['name']) + '\n')
        except (sd.PortAudioError, ValueError) as e:
            sys.stdout.write(
                style.WARNING(
                    'Warning: no compatible audio input devices found. '
                    'Audio recording will be disabled. Got {}\n'.format(str(e))))
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))
