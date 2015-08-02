# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0008_auto_20150731_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='golfer',
            name='player',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='golfer'),
        ),
    ]
