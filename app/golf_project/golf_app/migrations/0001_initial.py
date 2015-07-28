# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('course_name', models.CharField(max_length=150)),
                ('comment', models.TextField()),
                ('course_rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Golfer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('player', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hole',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('hole_number', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(18)])),
                ('par_type', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(5)])),
                ('hole_length', models.PositiveSmallIntegerField()),
                ('player_score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('green_in_regulation', models.BooleanField()),
                ('fairway_in_regulation', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scorecard',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('course_name', models.CharField(max_length=131)),
                ('course_length', models.PositiveSmallIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(to='golf_app.Golfer')),
            ],
        ),
        migrations.AddField(
            model_name='hole',
            name='scorecard',
            field=models.ForeignKey(to='golf_app.Scorecard'),
        ),
        migrations.AddField(
            model_name='comment',
            name='player',
            field=models.ForeignKey(to='golf_app.Golfer'),
        ),
    ]
