# health_records/views.py

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import HealthRecord, Prescription, Attachment
from .serializers import (
    HealthRecordSerializer, 
    PrescriptionSerializer, 
    AttachmentSerializer,
    HealthRecordWithPrescriptionsSerializer
)
from patients.models import Patient

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of a record to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator
        return obj.created_by == request.user

class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'record_type', 'record_date']
    search_fields = ['title', 'description', 'diagnosis', 'treatment', 'notes']
    ordering_fields = ['record_date', 'created_at']
    ordering = ['-record_date']
    
    def get_serializer_class(self):
        if self.action == 'create_with_prescriptions':
            return HealthRecordWithPrescriptionsSerializer
        return HealthRecordSerializer
    
    def get_queryset(self):
        """
        Filter health records:
        - Health professionals see all records they created
        - Patients see only their own records
        """
        user = self.request.user
        # Get patient records where the user is the patient's user
        patient_records = HealthRecord.objects.filter(patient__user=user)
        # Get records created by this user
        created_records = HealthRecord.objects.filter(created_by=user)
        # Combine and remove duplicates
        return (patient_records | created_records).distinct()
    
    @action(detail=False, methods=['post'])
    def create_with_prescriptions(self, request):
        """
        Create a health record with prescriptions in a single request
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def patient_history(self, request):
        """
        Get all health records for a specific patient
        """
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {"detail": "Patient ID is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Check if patient exists and user has access
            patient = Patient.objects.get(id=patient_id)
            user = request.user
            
            # Only allow access if user is the patient's user or a healthcare provider
            if patient.user != user and not HealthRecord.objects.filter(created_by=user).exists():
                return Response(
                    {"detail": "You do not have permission to access this patient's records."},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            queryset = HealthRecord.objects.filter(patient_id=patient_id).order_by('-record_date')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
                
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {"detail": "Patient not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['health_record']
    
    def get_queryset(self):
        """
        Filter prescriptions the same way as health records
        """
        user = self.request.user
        # Get prescriptions where the user is the patient's user
        patient_prescriptions = Prescription.objects.filter(health_record__patient__user=user)
        # Get prescriptions where the user created the health record
        created_prescriptions = Prescription.objects.filter(health_record__created_by=user)
        # Combine and remove duplicates
        return (patient_prescriptions | created_prescriptions).distinct()