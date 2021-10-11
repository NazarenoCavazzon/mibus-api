from django.contrib import admin
from .models import City, Company


admin.site.site_header = 'MIBUS Management'
admin.site.register(City)
admin.site.register(Company)


