# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0007_auto_20150730_0156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scorecard',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='golfer',
            name='player',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='golfer', null=True),
        ),
    ]
