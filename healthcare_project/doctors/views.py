from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Doctor, PatientDoctorMapping
from patients.models import Patient
from .serializers import DoctorSerializer, PatientDoctorMappingSerializer
from .filters import DoctorFilter

class IsOwnerOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to edit or delete it.
  """

  def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:
      return True

    # Instance must have an attribute named `owner`.
    if hasattr(obj, 'user'):
      return obj.user == request.user
    elif hasattr(obj, 'created_by'):
      return obj.created_by == request.user
    return False
  

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Doctor.objects.all()
    filterset_class = DoctorFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'specialization', 'hospital_affiliation']
    ordering_fields = ['first_name', 'last_name', 'experience_years', 'created_at']
    ordering = ['last_name', 'first_name']
    
    def get_queryset(self):
        """
        For listing doctors, everyone sees all doctors.
        For editing, users can only modify their own doctors.
        """
        if self.action == 'list':
            return Doctor.objects.all()
        else:
            user = self.request.user
            return Doctor.objects.filter(user=user)
        


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'doctor']
    
    def get_queryset(self):
        """
        This view returns a list of all mappings,
        or filtered by patient_id if provided in the URL.
        """
        queryset = PatientDoctorMapping.objects.all()
        patient_id = self.kwargs.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    