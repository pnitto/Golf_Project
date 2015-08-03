from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from statistics import mean
from rest_framework.compat import MinValueValidator, MaxValueValidator


class Golfer(models.Model):
    name = models.CharField(max_length=50)
    player = models.OneToOneField(User, related_name='golfer')
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}".format(self.name)

    @property
    def average_score(self):
        if self.scorecard_set.all().count() == 0:
            return 0
        else:
            value = []
            for x in self.scorecard_set.all():
                value.append(x.hole_score)
            return round(sum(value) / len(value), 1)

    @property
    def average_gir(self):
        if self.scorecard_set.all().count() == 0:
            return 0
        else:
            average = []
            for gir in self.scorecard_set.all():
                average.append(gir.gir_percentage)
            return round(sum(average) / len(average), 0)

    @property
    def average_fir(self):
        if self.scorecard_set.all().count() == 0:
            return 0
        else:
            average = []
            for fir in self.scorecard_set.all():
                average.append(fir.fir_percentage)
            return round(sum(average) / len(average), 0)


class ScorecardManager(models.Manager):

    def get_best_scorecard(self, player):
        scorecards = self.filter(player=player)
        sorted_list = sorted(scorecards, key=lambda scorecards:scorecards.hole_score)
        return sorted_list[0]


class Scorecard(models.Model):
    player = models.ForeignKey(Golfer, null=True)
    par_total = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(75)], null=True)
    course_name = models.CharField(max_length=131)
    course_length = models.PositiveSmallIntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']


    def __str__(self):
        return "{} - {}".format(self.course_name, self.timestamp)

    # It is counting any 3,4,5 as a par. I only want to count pars if player score is equal to par type on the instance
    @property
    def par_count(self):
        par_3_count = (self.hole_set.filter(par_type=3).exclude(par_type__in=[4,5]) and self.hole_set.filter(player_score=3).exclude(player_score__in=[4,5])).count()
        par_4_count = (self.hole_set.filter(par_type=4).exclude(par_type__in=[3,5]) and self.hole_set.filter(player_score=4).exclude(player_score__in=[3,5])).count()
        par_5_count = (self.hole_set.filter(par_type=5).exclude(par_type__in=[3,4]) and self.hole_set.filter(player_score=5).exclude(player_score__in=[3,4])).count()
        return sum([par_3_count, par_4_count, par_5_count])

    """def birdie_count(self):
        birdie_on_par_3 = (self.hole_set.filter(par_type=3).exclude(par_type__in=[4,5]) and self.hole_set.filter(player_score=2)).count()
        birdie_on_par_4 = (self.hole_set.filter(par_type=4).exclude(par_type__in=[3,5]) and self.hole_set.filter(player_score=3)).count()
        birdie_on_par_5 = (self.hole_set.filter(par_type=5).exclude(par_type__in=[3,4]) and self.hole_set.filter(player_score=4)).count()
        return sum([birdie_on_par_3, birdie_on_par_4, birdie_on_par_5])"""

    @property
    def hole_score(self):
        return sum(self.hole_set.all().exclude(player_score=None).values_list('player_score', flat=True))

    @property
    def gir_percentage(self):
       return round(sum(self.hole_set.all().exclude(green_in_regulation=None).values_list('green_in_regulation', flat=True)) * 100 / self.hole_set.count(), 0)

    @property
    def fir_percentage(self):
        if self.hole_set.filter(par_type__in=[4, 5]).count() == 0:
            return 0
        else:
            valid_par_count = self.hole_set.filter(par_type__in=[4, 5]).count()
            num_fir = sum(self.hole_set.filter(par_type__in=[4, 5]).exclude(fairway_in_regulation=None).values_list('fairway_in_regulation', flat=True))
            return round(num_fir / valid_par_count * 100, 0)

    @property
    def over_under_par(self):
        return sum(self.hole_set.all().exclude(player_score=None).values_list('player_score', flat=True)) - sum(self.hole_set.all().exclude(par_type=None).values_list('par_type', flat=True))


@receiver(post_save, sender=Scorecard, dispatch_uid="18_holes.post_save")
def instant_scorecard_creation(sender, instance, created, **kwargs):
    if created:
        for x in range(1,19):
            holes = Hole.objects.create(scorecard=instance, hole_number=x)
    return redirect('golf_app:scorecard_detail', instance.id)


class Hole(models.Model):
    scorecard = models.ForeignKey(Scorecard)
    hole_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(18)], null=True)
    par_type = models.PositiveSmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(5)], null=True)
    hole_length = models.PositiveSmallIntegerField(null=True)
    player_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], null=True)
    green_in_regulation = models.BooleanField(default=False)
    fairway_in_regulation = models.BooleanField(default=False )
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