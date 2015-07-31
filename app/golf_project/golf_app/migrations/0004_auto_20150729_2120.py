# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0003_auto_20150728_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hole',
            name='hole_number',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(18)], null=True),
        ),
        migrations.AlterField(
            model_name='hole',
            name='par_type',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(5)], null=True),
        ),
        migrations.AlterField(
            model_name='hole',
            name='player_score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], null=True),
        ),
    ]
