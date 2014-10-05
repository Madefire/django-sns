# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Notification.topicArn'
        db.alter_column(u'sns_notification', 'topicArn', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Changing field 'Notification.subject'
        db.alter_column(u'sns_notification', 'subject', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Subscription.token'
        db.alter_column(u'sns_subscription', 'token', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'Subscription.signature'
        db.alter_column(u'sns_subscription', 'signature', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Subscription.message'
        db.alter_column(u'sns_subscription', 'message', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Subscription.topicArn'
        db.alter_column(u'sns_subscription', 'topicArn', self.gf('django.db.models.fields.CharField')(max_length=256))

    def backwards(self, orm):

        # Changing field 'Notification.topicArn'
        db.alter_column(u'sns_notification', 'topicArn', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Notification.subject'
        db.alter_column(u'sns_notification', 'subject', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Subscription.token'
        db.alter_column(u'sns_subscription', 'token', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Subscription.signature'
        db.alter_column(u'sns_subscription', 'signature', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Subscription.message'
        db.alter_column(u'sns_subscription', 'message', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Subscription.topicArn'
        db.alter_column(u'sns_subscription', 'topicArn', self.gf('django.db.models.fields.CharField')(max_length=250))

    models = {
        u'sns.notification': {
            'Meta': {'object_name': 'Notification'},
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'messageId': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '9'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'topicArn': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'sns.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'messageId': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signatureVersion': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'signingCertURL': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '7'}),
            'subscribeURL': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'topicArn': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['sns']