from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor

class HealthRecord(models.Model):
  RECORD_TYPES = (
    ('consultation', 'Consultation'),
    ('lab_results', 'Lab Results'),
    ('prescription', 'Prescription'),
    ('imaging', 'Imaging'),
    ('surgery', 'Surgery'),
    ('vaccination', 'Vaccination'),
    ('other', 'Other')
  )

  patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_records')
  doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='health_records')
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_health_records')
  record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
  record_date = models.DateTimeField()
  title = models.CharField(max_length=200)
  description = models.TextField()
  diagnosis = models.TextField(blank=True, null=True)
  treatment = models.TextField(blank=True, null=True)
  notes = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.patient} ({self.record_date.strftime('%Y-%m-%d')})"
  
class Prescription(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.medication_name} - {self.dosage}"

class Attachment(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='attachments')
    title = models.CharField(max_length=100)
    file_type = models.CharField(max_length=50)
    file_path = models.TextField()  # In a real app, you'd use FileField
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_attachments')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# Create your models here.
