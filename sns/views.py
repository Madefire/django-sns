'''
Created on July, 15th 2013


@author: thanos
'''


import logging
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .helpers import verify_signature
from .models import Subscription, Notification

logger = logging.getLogger(__name__)


@csrf_exempt
@transaction.atomic
def sns_endpoint(request):
    message = json.loads(request.body)
    msg_type = message['Type']
    if msg_type == 'SubscriptionConfirmation':
        keys = (
            'Message',
            'MessageId',
            'SubscribeURL',
            'Timestamp',
            'Token',
            'TopicArn',
            'Type',
        )
        if not verify_signature(keys, message):
            return HttpResponseBadRequest()
        obj = Subscription.process(message)
    elif msg_type == 'Notification':
        obj = Notification.add(message)
        keys = (
            'Message',
            'MessageId',
            'Subject',
            'Timestamp',
            'TopicArn',
            'Type',
        )
        if not verify_signature(keys, message):
            return HttpResponseBadRequest()
    else:
        logger.error('Unknown message type %s: message=%s', message['Type'], message)
        return HttpResponseBadRequest('Unknown Request')
    return HttpResponse(
        json.dumps({'status': obj.status, 'message': message}),
        content_type="application/json")


@staff_member_required
@transaction.atomic
def subscribe(request, topic):
    default_host = '%s://%s' % (request.META.get('wsgi.url_scheme', 'https'),
                                request.META['HTTP_HOST'])
    browse_host = request.META.get('HTTP_ORIGIN', default_host)
    protocal, dev_null = browse_host.split('://')
    subscription = Subscription.subscribe(topic, protocal, browse_host)
    return HttpResponse(subscription.message, content_type="application/json")
