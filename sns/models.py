'''
Created on July, 15th 2013


@author: thanos
'''

import boto
import boto.sns
import datetime
import json
import logging
import requests


from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from .signals import sns_signal


logger = logging.getLogger(__name__)


class Subscription(models.Model):
    """
    {
    "Type" : "SubscriptionConfirmation",
    "MessageId" : "165545c9-2a5c-472c-8df2-7ff2be2b3b1b",
    "Token" : "2336412f37fb687f5d51e6785c03b0879594eeac82c01f235d0e717736",
    "TopicArn" : "arn:aws:sns:us-east-1:123456789012:MyTopic",
    "Message" : "You have chosen to subscribe to the topic arn:aws:sns:us-east-1:1212:MyTopic.\n...visit the SubscribeURL included in this message",
    "SubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=ConfirmSubscription&TopicArn=arn:aws:sns:us-east-1:11231:MyTopic&Token=23366",
    "Timestamp" : "2012-04-26T20:45:04.751Z",
    "SignatureVersion" : "1",
    "Signature" : "EXAMPLEpH+D61GWB6jI9b5+gLPoBc1Q=",
    "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-fde52f.pem"
    }

    """

    STATUS_ACTIVE = 'ACTIVE'
    STATUS_PENDING = 'PENDING'
    STATUS_RETIRED = 'RETIRED'
    STATUSES = (STATUS_ACTIVE, STATUS_PENDING, STATUS_RETIRED)

    topic = models.CharField(max_length=128)
    messageId = models.CharField(max_length=48)
    token = models.CharField(max_length=256, null=True, blank=True)
    topicArn = models.CharField(max_length=256)
    message = models.TextField()
    subscribeURL = models.URLField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField()
    signatureVersion = models.CharField(max_length=32, null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    signingCertURL = models.URLField(max_length=512, null=True, blank=True)
    status = models.CharField(max_length=max(map(len, STATUSES)),
                              choices=zip(STATUSES, map(lambda x: x.capitalize(), STATUSES)),
                              default=STATUS_PENDING)
    modified = models.DateTimeField(auto_now=True)
    errors = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{} ({}:{})".format(self.topicArn,  self.status, self.modified)

    @classmethod
    def process(cls, message):
        topicArn = message['TopicArn']
        topic = topicArn.split(':')[-1]
        try:
            subscription = Subscription.objects.get(topicArn=topicArn)
        except Subscription.DoesNotExist:
            subscription = Subscription(topicArn=topicArn)
        subscription.topic = topic
        subscription.messageId = message["MessageId"]
        subscription.token = message["Token"]
        subscription.message = message["Message"]
        subscription.subscribeURL = message["SubscribeURL"]
        subscription.timestamp = message["Timestamp"]
        subscription.signatureVersion = message["SignatureVersion"]
        subscription.signature = message["Signature"]
        subscription.signingCertURL = message["SigningCertURL"]
        subscription.status = cls.STATUS_ACTIVE
        requests.get(message['SubscribeURL'])
        logger.info('GET SubscribeURL %s', message['SubscribeURL'])
        subscription.save()
        return subscription

    @classmethod
    def get_topicarn(cls, topic_label):
        response = cls.aws_connection(topic_label).get_all_topics()
        for topic in response['ListTopicsResponse']['ListTopicsResult']['Topics']:
            if topic['TopicArn'].endswith(topic_label):
                return topic['TopicArn']
    _aws_connection = None

    @classmethod
    def aws_connection(cls, topic_label):
        if not cls._aws_connection:
            for r in boto.sns.regions():
                if (':%s:' % r.name) in topic_label:
                    region = r
                    break
            cls._aws_connection = boto.connect_sns(settings.AWS_ACCESS_KEY_ID,
                                                   settings.AWS_SECRET_ACCESS_KEY, region=region)
        return cls._aws_connection

    @classmethod
    def subscribe(cls, topic_label, protocol, browse_host):
        '''
        {u'SubscribeResponse': {
            u'SubscribeResult': {u'SubscriptionArn': u'pending confirmation'},
            u'ResponseMetadata': {u'RequestId': u'01d0e9c4-e566-569b-b9c9-a39aa65e2507'}}
        }
        '''
        endpoint_url = browse_host + reverse("sns_endpoint")
        response = cls.aws_connection(topic_label).subscribe(topic_label, protocol, endpoint_url)

        return Subscription.objects.create(
                topic=topic_label,
                messageId=response['SubscribeResponse']['ResponseMetadata']['RequestId'],
                topicArn=cls.get_topicarn(topic_label),
                message=json.dumps(response),
                timestamp=datetime.datetime.utcnow(),
                )


class Notification(models.Model):
    """
    {
    "Type" : "Notification",
    "MessageId" : "22b80b92-fdea-4c2c-8f9d-bdfb0c7bf324",
    "TopicArn" : "arn:aws:sns:us-east-1:123456789012:MyTopic",
    "Subject" : "My First Message",
    "Message" : "Hello world!",
    "Timestamp" : "2012-05-02T00:54:06.655Z",
    "SignatureVersion" : "1",
    "Signature" : "EXAMPLErk9ZiPph5YlLmWsDcyC5T+Sy9/umic5S0UQc2PEtgdpVBahwNOdMW4JPwk0kAJJztnc=",
    "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-f3e52f.pem",
    "UnsubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:123456789012:MyTopic:c9136"
    }
    """

    STATUS_PENDING = 'PENDING'
    STATUS_PROCESSED = 'PROCESSED'
    STATUS_ERROR = 'ERROR'
    STATUSES = (STATUS_PENDING, STATUS_PROCESSED, STATUS_ERROR)

    messageId = models.CharField(max_length=48)
    topicArn = models.CharField(max_length=256)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField()
    status = models.CharField(
        max_length=max(map(len, STATUSES)),
        choices=zip(STATUSES, map(lambda x: x.capitalize(), STATUSES)),
        default=STATUS_PENDING)
    modified = models.DateTimeField(auto_now=True)
    errors = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{}: {} ({}:{})".format(self.topicArn, self.subject,   self.status, self.modified)

    @classmethod
    def add(cls, message):
        if getattr(settings, 'SNS_SAVE_NOTIFICATIONS', True):
            notification = Notification.objects.create(
                    messageId=message["MessageId"],
                    topicArn=message["TopicArn"],
                    subject=message.get("Subject", message["Message"])[:100],
                    message=message["Message"],
                    timestamp=message["Timestamp"],
            )
        sns_signal.send(cls, message=message)
        return notification
