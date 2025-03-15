from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
  GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
  )

  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  date_of_birth = models.DateField()
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  contact_number = models.CharField(max_length=15)
  email = models.EmailField(blank=True, null=True)
  address = models.TextField()
  medical_history = models.TextField(blank=True, null=True)
  insurance_info = models.TextField(blank=True, null=True, max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self):
    return f"{self.first_name} {self.last_name}"