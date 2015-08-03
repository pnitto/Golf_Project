# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0009_auto_20150731_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='golfer',
            name='player',
            field=models.ForeignKey(related_name='golfer', to=settings.AUTH_USER_MODEL),
        ),
    ]
