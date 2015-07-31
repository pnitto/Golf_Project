# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0004_auto_20150729_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hole',
            name='fairway_in_regulation',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hole',
            name='green_in_regulation',
            field=models.BooleanField(default=False),
        ),
    ]
