from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from statistics import mean
from rest_framework.compat import MinValueValidator, MaxValueValidator
from rest_framework.reverse import reverse


class Golfer(models.Model):
    name = models.CharField(max_length=50)
    player = models.OneToOneField(User, related_name='golfer', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}".format(self.name)

    @property
    def par_type_list(self):
        par_type = self.scorecard_set.all().values_list('par_total')
        return [i[0] for i in par_type]

    @property
    def scorecard_names(self):
        names = self.scorecard_set.all().values_list('course_name')
        return [str(i[0]) for i in names]

    @property
    def scores_for_scorecards(self):
        value = []
        for x in self.scorecard_set.all():
            value.append(x.hole_score)
        return value


    @property
    def gir_for_scorecards(self):
        value = []
        for x in self.scorecard_set.all():
            value.append(x.gir_percentage)
        return value

    @property
    def fir_for_scorecards(self):
        value = []
        for x in self.scorecard_set.all():
            value.append(x.fir_percentage)
        return value

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

    def top_5_player_scores(self,player):
        scorecards = self.filter(player=player)
        sorted_list = sorted(scorecards, key=lambda scorecards:scorecards.hole_score)
        return sorted_list[::-1][:5]

    def top_5_gir(self,player):
        scorecards = self.filter(player=player)
        sorted_list = sorted(scorecards, key=lambda scorecards:scorecards.gir_percentage)
        return sorted_list[::-1][:5]

    def top_5_fir(self,player):
        scorecards = self.filter(player=player)
        sorted_list = sorted(scorecards, key=lambda scorecards:scorecards.fir_percentage)
        return sorted_list[::-1][:5]



class Scorecard(models.Model):
    player = models.ForeignKey(Golfer, null=True,on_delete=models.CASCADE)
    par_total = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(75)], null=True)
    course_name = models.CharField(max_length=131)
    course_length = models.PositiveSmallIntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ScorecardManager()

    class Meta:
        ordering = ['-timestamp']


    def __str__(self):
        return "{}".format(self.course_name)

    @property
    def par_count(self):
        par_count = (self.hole_set.filter(par_type=F('player_score'))).count()
        return par_count

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
    scorecard = models.ForeignKey(Scorecard,on_delete=models.CASCADE)
    hole_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(18)], null=True)
    par_type = models.PositiveSmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(5)], null=True)
    hole_length = models.PositiveSmallIntegerField(null=True)
    player_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], null=True)
    green_in_regulation = models.BooleanField(default=False)
    fairway_in_regulation = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['hole_number']

    def bool_cleaner(self, field):
        return "Yes" if field else "No"

    @property
    def gir(self):
        return self.bool_cleaner(self.green_in_regulation)

    @property
    def fir(self):
        return self.bool_cleaner(self.fairway_in_regulation)

    @property
    def previous_hole(self):
        return Hole.objects.get(scorecard=self.scorecard,hole_number=self.hole_number - 1)

    @property
    def next_hole(self):
         return Hole.objects.get(scorecard=self.scorecard,hole_number=self.hole_number + 1)

    @property
    def hole_over_under_par(self):
        if self.player_score and self.par_type:
            return self.player_score - self.par_type
        else:
            return


class Comment(models.Model):
    player = models.ForeignKey(Golfer,on_delete=models.CASCADE)
    course_name = models.CharField(max_length=150)
    comment  = models.TextField()
    course_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
