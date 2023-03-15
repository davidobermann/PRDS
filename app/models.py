import datetime
import django
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    '''
    There are 2 types of goals:
    - Fincancial (FI): Reach a certain amount of money
    - Frequency (FQ): Travel a certain amount of times
    Limits is the time limitation in days from the creation timepoint on to be reached
    When the value is 0 there is no limit.
    - If FI then with the sum of money traveled inbetween the start point of the goal to the limit days
    - If FQ how many journeys should be taken until the goal expires
    '''

    class GoalType(models.TextChoices):
        FI = "FI", "Financial Goal"
        FQ = "FQ", "Frequency Goal"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False) # if true display this on the main screen
    timestamp = models.DateTimeField(default=django.utils.timezone.now) # creation date
    progress = models.IntegerField(default=0) # the progress made

    name = models.CharField(max_length=255, default='New Goal') # the name of the goal
    type = models.CharField(max_length=2, choices=GoalType.choices)  # Financial, Frequency
    criteria = models.IntegerField()  # the value to be reached to fulfill the goal
    startdate = models.DateField(blank=True, null=True)  # when the goal should start to be set out
    enddate = models.DateField(blank=True, null=True) # when the goal should be reached


class Journey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    price = models.FloatField()
    date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        print('')
        return self.user +\
            ' from ' +\
            self. origin +\
            ' to ' +\
            self.destination +\
            ' on ' +\
            self.date +\
            ' for ' +\
            self.price