from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient

class Doctor(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  specialization = models.CharField(max_length=100)
  license_number = models.CharField(max_length=50, unique=True)
  contact_number = models.CharField(max_length=15)
  email = models.EmailField()
  experience_years = models.PositiveIntegerField()
  hospital_affiliation = models.CharField(max_length=100, blank=True, null=True)
  available_days = models.CharField(max_length=100, blank=True, null=True)
  # address = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name} ({self.specialization})"
  
class PatientDoctorMapping(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctors_mappings')
  doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients_mappings')
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_mappings')
  notes = models.TextField(blank=True, null=True)
  # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ('patient', 'doctor')

  def __str__(self):
    return f"Patient: {self.patient} - Doctor: {self.doctor}"