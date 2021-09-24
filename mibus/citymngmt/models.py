from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ClientUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    isCity = models.BooleanField(default=True)
    def __str__(self):
        return str(self.user)

class CitySession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

class CompanyRelations(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    client = models.ForeignKey('ClientUser', on_delete=models.CASCADE, null=True)
    password = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.company) + " - " + str(self.client)

class City(models.Model):
    activated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=50)
    polygon = models.TextField(default="")
    status = models.BooleanField(default=False)
    image = models.TextField(default="")

class Company(models.Model):
    activated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.TextField(max_length=50)
    color = models.TextField(default="")

class Line(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.TextField(max_length=50)
    stops = models.TextField(default="")
    zone_times = models.TextField(default="")
    round_trip = models.TextField(default="")
    return_trip = models.TextField(default="")
    special_round_trip = models.TextField(default="")
    special_return_trip = models.TextField(default="")
    status = models.BooleanField(default=False)

class BusStop(models.Model):
    relation = models.ForeignKey(CompanyRelations, on_delete=models.CASCADE, null=True)
    lines = models.TextField(default="")
    name = models.TextField(max_length=50)
    subtitle = models.TextField(default="")
    address = models.TextField(default="")
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)