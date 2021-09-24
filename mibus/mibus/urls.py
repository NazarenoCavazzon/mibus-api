from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path
import mibus.views as views
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login_view),
    path('register', views.register_view),
    path('register/company', views.register_company_view),
    path('home', views.home_view),
    path('', views.home_view),
    path('main', views.main_view),
    path('main-company', views.main_view_company),
    path('logout', views.logout_view),
    path('city/<int:id>', views.edit_city_view),
    path('cities/<int:id>', views.edit_cities_view),
    path('cities/verify/<int:relation_id>', views.access_cities_view),
    path('company/<int:id>', views.edit_company_view),
    path('companies/<int:id>', views.edit_companies_view),
    path('setbusstops/<int:relation_id>', views.set_busstops_view),
    path('editline/<int:line_id>', views.edit_line_view),
    path('companies/addcompany/<int:id>', views.add_companies_view),
    path('addline/<int:relation_id>', views.add_lines_view),
    path('companies/delete/<int:relation_id>', views.delete_company_view),
    path('cities/editlines/<int:relation_id>', views.edit_cities_lines_view),
    path('companies/editcompany/<int:relation_id>', views.edit_company_forCity_view),
]
