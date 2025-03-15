# health_records/serializers.py

from rest_framework import serializers
from .models import HealthRecord, Prescription, Attachment
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ('health_record', 'created_at', 'updated_at')

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = ('health_record', 'uploaded_by', 'uploaded_at')

class HealthRecordSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = HealthRecord
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Assign the current user as the creator
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ('medication_name', 'dosage', 'frequency', 'duration', 'instructions')

class HealthRecordWithPrescriptionsSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionCreateSerializer(many=True)
    
    class Meta:
        model = HealthRecord
        fields = ('patient', 'doctor', 'record_type', 'record_date', 'title', 
                  'description', 'diagnosis', 'treatment', 'notes', 'prescriptions')
    
    def create(self, validated_data):
        prescriptions_data = validated_data.pop('prescriptions')
        # Assign the current user as the creator
        validated_data['created_by'] = self.context['request'].user
        health_record = HealthRecord.objects.create(**validated_data)
        
        # Create prescriptions for this health record
        for prescription_data in prescriptions_data:
            Prescription.objects.create(health_record=health_record, **prescription_data)
            
        return health_record