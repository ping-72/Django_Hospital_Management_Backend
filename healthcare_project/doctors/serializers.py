from rest_framework import serializers
from .models import Doctor, PatientDoctorMapping
from patients.models import Patient
from patients.serializers import PatientSerializer

class DoctorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Doctor
    fields = '__all__'
    read_only_fields = ('user','created_at', 'updated_at')

  def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    return super().create(validated_data)
  
class PatientDoctorMappingSerializer(serializers.ModelSerializer):
  patient_details = PatientSerializer(source='patient', read_only=True)
  doctor_details = DoctorSerializer(source='doctor', read_only=True)

  class Meta:
    model = PatientDoctorMapping
    fields = ['id', 'patient', 'doctor', 'notes', 'created_at', 'updated_at', 'patient_details', 'doctor_details']
    read_only_fields = ('created_at', 'updated_at', 'created_by')

  def create(self, validated_data):
    validated_data['created_by'] = self.context['request'].user
    return super().create(validated_data)
  
  