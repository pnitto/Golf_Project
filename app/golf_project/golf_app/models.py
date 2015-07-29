from django.contrib.auth.models import User
from django.db import models
from rest_framework.compat import MinValueValidator, MaxValueValidator


class Golfer(models.Model):
    name = models.CharField(max_length=50)
    player = models.OneToOneField(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Scorecard(models.Model):
    player = models.ForeignKey(Golfer, null=True)
    course_name = models.CharField(max_length=131)
    course_length = models.PositiveSmallIntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.course_name, self.timestamp)


class Hole(models.Model):
    scorecard = models.ForeignKey(Scorecard)
    hole_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(18)])
    par_type = models.PositiveSmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(5)]) # need to make this (3, 4, or 5)
    hole_length = models.PositiveSmallIntegerField(null=True)
    player_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)]) # need to make this between 1 - 10
    green_in_regulation = models.BooleanField()
    fairway_in_regulation = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['hole_number']


class Comment(models.Model):
    player = models.ForeignKey(Golfer)
    course_name = models.CharField(max_length=150)
    comment  = models.TextField()
    course_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']