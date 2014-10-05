'''
Created on July, 15th 2013


@author: thanos
'''


import logging, json
logger = logging.getLogger(__name__)

from time import sleep


from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import Subscription, Notification


@csrf_exempt
def sns_endpoint(request):
    message = json.loads(request.raw_post_data)
    if message['Type'] == 'SubscriptionConfirmation':
        sleep(5)
        obj = Subscription.process(message)
    elif message['Type'] == 'Notification':
        obj= Notification.add(message)
    else:
        return HttpResponseBadRequest('Unknown Request')
    return HttpResponse(json.dumps({'status': obj.status, 'message':message}), mimetype="application/json")


@staff_member_required
def subscribe(request, topic):
    browse_host = request.META.get('HTTP_ORIGIN', '%s://%s' %
                                    (request.META.get('wsgi.url_scheme', 'https'),
                                        request.META['HTTP_HOST']))
    protocal, dev_null = browse_host.split('://')
    subscription = Subscription.subscribe(topic, protocal, browse_host)
    return HttpResponse(subscription.message, mimetype="application/json")