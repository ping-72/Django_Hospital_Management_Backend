from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Patient
    fields = '__all__'
    read_only_fields = ('user','created_at', 'updated_at')

  def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    return super().create(validated_data)