from .views import RegisterCompanyViewSet
from rest_framework.routers import DefaultRouter 

router = DefaultRouter()
router.register(r'registerCompany', RegisterCompanyViewSet, basename='registerCompany')