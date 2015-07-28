# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='hole',
            options={'ordering': ['hole_number']},
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='course_length',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='player',
            field=models.ForeignKey(to='golf_app.Golfer', null=True),
        ),
    ]
