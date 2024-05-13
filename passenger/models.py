from django.db import models
from base.models import BaseModel

class Passenger(BaseModel):
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)
    MiddleName = models.CharField(max_length=255, null=True, blank=True)
    EmailAddress = models.EmailField(max_length=255)
    DateOfBirth = models.DateField()
    PhoneNumber = models.CharField(max_length=255, null=True, blank=True)
    Nationality = models.CharField(max_length=255, null=True, blank=True)
    Gender = models.CharField(max_length=100, default="Other")
    EmergencyContact = models.OneToOneField('EmergencyContact', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.FirstName} {self.LastName} ({self.EmailAddress})"

class EmergencyContact(BaseModel):
    FullName = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    PhoneNumber = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.FullName} ({self.Email})"
