# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0005_auto_20150729_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorecard',
            name='par_total',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(75)], null=True),
        ),
    ]
