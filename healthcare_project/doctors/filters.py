# doctors/filters.py

import django_filters
from .models import Doctor

class DoctorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    specialization = django_filters.CharFilter(lookup_expr='icontains')
    min_experience = django_filters.NumberFilter(field_name='experience_years', lookup_expr='gte')
    max_experience = django_filters.NumberFilter(field_name='experience_years', lookup_expr='lte')
    hospital = django_filters.CharFilter(field_name='hospital_affiliation', lookup_expr='icontains')
    
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization']