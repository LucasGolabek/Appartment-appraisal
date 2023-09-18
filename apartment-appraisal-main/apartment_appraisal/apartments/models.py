from django.contrib.auth.models import User
from django.db import models


class UserApartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    measurement = models.FloatField(blank=False)
    location = models.CharField(max_length=80, blank=False)
    rooms = models.IntegerField(blank=False)
    heating = models.CharField(max_length=32, blank=True)


class CollectedApartment(models.Model):
    url = models.CharField(primary_key=True, max_length=80, blank=False)
    price = models.FloatField(blank=False)
    measurement = models.FloatField(blank=False)
    rooms = models.IntegerField(blank=False)
    heating = models.CharField(max_length=32, blank=True, null=True, default=None)
    is_checked = models.BooleanField(default=False)

    location = models.CharField(max_length=120, blank=False)
    latitude = models.FloatField(blank=True, null=True) # szerokość geograficzna (N, S)
    longitude = models.FloatField(blank=True, null=True) # długość geograciczna (W, E)
