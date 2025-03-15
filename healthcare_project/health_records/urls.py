# health_records/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthRecordViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register(r'health-records', HealthRecordViewSet, basename='health-record')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    path('', include(router.urls)),
]