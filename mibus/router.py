from .views import RegisterCompanyViewSet, CitiesViewSet, BusStopViewSet
from rest_framework.routers import DefaultRouter 

router = DefaultRouter()
router.register(r'registerCompany', RegisterCompanyViewSet, basename='registerCompany')
router.register(r'cities', CitiesViewSet, basename='cities')
router.register(r'busStops', BusStopViewSet, basename='busStops')