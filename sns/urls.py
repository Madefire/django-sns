from django.conf.urls import url
from sns.views import sns_endpoint, subscribe

urlpatterns = [
    url(r'^$', sns_endpoint, name='sns_endpoint'),
    url(r'^subscribe/(?P<topic>[^/]+)/$', subscribe, name='subscribe'),
]
