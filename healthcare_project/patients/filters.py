# patients/filters.py

import django_filters
from .models import Patient

class PatientFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    min_age = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='year__lte', 
                                        label='Minimum Age (years)')
    max_age = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='year__gte', 
                                        label='Maximum Age (years)')
    gender = django_filters.ChoiceFilter(choices=Patient.GENDER_CHOICES)
    
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'gender']