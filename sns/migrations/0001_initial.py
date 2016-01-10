# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('messageId', models.CharField(max_length=48)),
                ('topicArn', models.CharField(max_length=256)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('status', models.CharField(default=b'PENDING', max_length=9, choices=[(b'PENDING', b'Pending'), (b'PROCESSED', b'Processed'), (b'ERROR', b'Error')])),
                ('modified', models.DateTimeField(auto_now=True)),
                ('errors', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=128)),
                ('messageId', models.CharField(max_length=48)),
                ('token', models.CharField(max_length=256, null=True, blank=True)),
                ('topicArn', models.CharField(max_length=256)),
                ('message', models.TextField()),
                ('subscribeURL', models.URLField(max_length=512, null=True, blank=True)),
                ('timestamp', models.DateTimeField()),
                ('signatureVersion', models.CharField(max_length=32, null=True, blank=True)),
                ('signature', models.TextField(null=True, blank=True)),
                ('signingCertURL', models.URLField(max_length=512, null=True, blank=True)),
                ('status', models.CharField(default=b'PENDING', max_length=7, choices=[(b'ACTIVE', b'Active'), (b'PENDING', b'Pending'), (b'RETIRED', b'Retired')])),
                ('modified', models.DateTimeField(auto_now=True)),
                ('errors', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
