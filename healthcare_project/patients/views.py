from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PatientSerializer
from .models import Patient
from .filters import PatientFilter

class IsOwnerOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to edit it.
  """

  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    
    # Write permissions are only allowed to the owner of the patient.
    return obj.user == request.user
  

class PatientViewSet(viewsets.ModelViewSet):
  serializer_class = PatientSerializer
  permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
  filterset_class = PatientFilter
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['first_name', 'last_name', 'email', 'medical_history']
  ordering_fields = ['first_name', 'last_name', 'created_at']
  ordering = ['created_at']

  def get_queryset(self):
    """
    This returns a list of all the patients for the currently authenticated user.
    """
    user = self.request.user
    return Patient.objects.filter(user=user)
# Create your views here.
