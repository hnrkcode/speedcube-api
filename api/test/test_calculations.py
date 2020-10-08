from django.test import TestCase

from api.calculations import average_time, best_time, median_time, worst_time
from api.models import TimeModel, UserModel


class TestCalculations(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserModel.objects.create_user(
            username="test", email="test@test.com", password="test"
        )

        TimeModel.objects.create(
            user=UserModel.objects.get(id=1),
            time=111,
            dnf=False,
            penalty=False,
        )
        TimeModel.objects.create(
            user=UserModel.objects.get(id=1),
            time=200,
            dnf=False,
            penalty=False,
        )
        TimeModel.objects.create(
            user=UserModel.objects.get(id=1),
            time=300,
            dnf=False,
            penalty=False,
        )
        TimeModel.objects.create(
            user=UserModel.objects.get(id=1),
            time=1234,
            dnf=False,
            penalty=False,
        )

    def test_best_time(self):
        times = TimeModel.objects.filter(user=1)
        self.assertEquals(best_time(times), 111)

    def test_worst_time(self):
        times = TimeModel.objects.filter(user=1)
        self.assertEquals(worst_time(times), 1234)

    def test_average_time(self):
        times = TimeModel.objects.filter(user=1)
        self.assertEquals(average_time(times), 461)

    def test_median_time(self):
        times = TimeModel.objects.filter(user=1)
        self.assertEquals(median_time(times), 250)
