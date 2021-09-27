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
    def __str__(self):
        return str(self.user)

class CompanyRelations(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    client = models.ForeignKey('ClientUser', on_delete=models.CASCADE, null=True)
    password = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.company) + " - " + str(self.client)

class City(models.Model):
    activated = models.BooleanField(default=False, required=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, required=False)
    ticket_price = models.IntegerField(default=0, required=False)
    emergency_phone = models.CharField(max_length=100, default="", required=False)
    name = models.TextField(max_length=50, required=False)
    polygon = models.JSONField(null=True, required=False)
    status = models.BooleanField(default=False, required=False)
    image = models.TextField(default="", required=False)
    def __str__(self):
        return str(self.user)

class Company(models.Model):
    activated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.TextField(max_length=50)
    color = models.TextField(default="")
    def __str__(self):
        return str(self.user)

class Line(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    relation = models.ForeignKey(CompanyRelations, on_delete=models.CASCADE, null=True)
    schedule = models.JSONField(null=True)
    name = models.TextField(max_length=50)
    stops = models.JSONField(null=True)
    zone_times = models.JSONField(null=True)
    round_trip = models.JSONField(null=True)
    return_trip = models.JSONField(null=True)
    special_round_trip = models.JSONField(null=True)
    special_return_trip = models.JSONField(null=True)
    status = models.BooleanField(default=False)

class BusStops(models.Model):
    relation = models.ForeignKey(CompanyRelations, on_delete=models.CASCADE, null=True)
    busStops = models.JSONField(null=True)