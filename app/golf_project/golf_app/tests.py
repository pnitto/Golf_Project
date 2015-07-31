from django.test import TestCase

# Create your tests here.
from golf_app.models import Scorecard, Hole


class ScorecardModelTests(TestCase):


    def test_creating_a_score_card_creates_18_holes(self):
        Scorecard.objects.create(course_name="Joel Golf")
        hole_count = Hole.objects.count()
        self.assertEqual(hole_count, 18)

    def test_creating_a_score_card_creates_18_holes_associated_with_scorecard(self):
        sut_card = Scorecard.objects.create(course_name="Joel Golf")
        Scorecard.objects.create(course_name="Paul Golf")

        hole_count = sut_card.hole_set.count()
        self.assertEqual(hole_count, 18)
        all_hole_count = Hole.objects.count()
        self.assertEqual(all_hole_count, 18 * 2)

    def test_fir_percentage_is_0_if_no_par4_or_par5(self):
        scorecard = Scorecard.objects.create(course_name="Paul Golf")
        scorecard.hole_set.update(par_type=3)
        self.assertEqual(scorecard.fir_percentage, 0)

    def test_fir_percentage_is_50_if_all_par4_and_half_in_regulation(self):
        scorecard = Scorecard.objects.create(course_name="Paul Golf")
        scorecard.hole_set.update(par_type=4)
        holes = scorecard.hole_set.filter(hole_number__in=range(1, 10))
        holes.update(fairway_in_regulation=True)
        self.assertEqual(scorecard.fir_percentage, 50)

    def test_fir_percentage_is_50_if_all_par5_and_half_in_regulation(self):
        scorecard = Scorecard.objects.create(course_name="Paul Golf")
        scorecard.hole_set.update(par_type=5)
        holes = scorecard.hole_set.filter(hole_number__in=range(1, 10))
        holes.update(fairway_in_regulation=True)
        self.assertEqual(scorecard.fir_percentage, 50)