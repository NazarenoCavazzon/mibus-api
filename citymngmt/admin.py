from django.contrib import admin
from . import models
# Register your models here.
class CityAdmin(admin.AdminSite):
    site_header = 'City Management'

city_site = CityAdmin(name="CityAdmin")
city_site.register(models.City)


