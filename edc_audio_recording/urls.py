from django.conf.urls import url

from .admin import recording_admin
from .views import RecordView, PlaybackView


urlpatterns = [
    url(r'^record/(?P<app_label>.*)/(?P<model_name>.*)/'
        '(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/',
        RecordView.as_view(), name='record'),
    url(r'^play/(?P<app_label>.*)/(?P<model_name>.*)/'
        '(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/',
        PlaybackView.as_view(), name='play'),
    url('^admin/', recording_admin.urls),
    url('^', recording_admin.urls),
]
