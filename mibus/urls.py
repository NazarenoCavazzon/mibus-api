from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path
from citymngmt.admin import city_site
import mibus.views as views
from .router import router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls, name='admin'),
    path('admin/cities', city_site.urls, name='admin'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('register/company', views.register_company_view, name='register_company'),
    path('home', views.home_view, name='home'),
    path('', views.home_view),
    path('main', views.main_view, name='main_city_view'),
    path('main-company', views.main_view_company, name='main_company_view'),
    path('logout', views.logout_view, name='logout'),
    path('city/<int:id>', views.edit_city_view, name='edit_city_view'),
    path('cities/<int:id>', views.edit_cities_view, name='edit_cities_view'),
    path('cities/verify/<int:relation_id>', views.access_cities_view, name='access_cities_view'),
    path('company/<int:id>', views.edit_company_view, name='edit_company_view'),
    path('companies/<int:id>', views.edit_companies_view, name='edit_companies_view'),
    path('setbusstops/<int:relation_id>', views.set_busstops_view, name='set_busstops_view'),
    path('editline/<int:line_id>', views.edit_line_view, name='edit_line_view'),
    path('companies/addcompany/<int:id>', views.add_companies_view, name='add_companies_view'),
    path('addline/<int:relation_id>', views.add_lines_view, name='add_lines_view'),
    path('companies/delete/<int:relation_id>', views.delete_company_view, name='delete_company_view'),
    path('cities/editlines/<int:relation_id>', views.edit_cities_lines_view, name='edit_cities_lines_view'),
    path('companies/editcompany/<int:relation_id>', views.edit_company_forCity_view, name='edit_company_forCity_view'),
    path('getAllStops', views.getAllStops),
    path('getCityCompanies/<int:city_id>', views.getCityCompanies),
    path('getCityLines/<int:city_id>', views.getCityLines),
    path('getCompany/<int:company_id>', views.getCompany),
]
