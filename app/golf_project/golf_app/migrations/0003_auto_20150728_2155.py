# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0002_auto_20150727_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hole',
            name='hole_length',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
