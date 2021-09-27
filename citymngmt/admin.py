from django.contrib import admin
from . import models
# Register your models here.
class CityAdmin(admin.ModelAdmin):
    site_header = 'City Management'

city_site = CityAdmin(name='BlogAdmin')
city_site.register(models.City)


