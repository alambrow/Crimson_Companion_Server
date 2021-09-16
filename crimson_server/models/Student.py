from crimson_server.models.CrimsonUser import CrimsonUser
from django.db import models

class Student(models.Model):
    user = models.ForeignKey("CrimsonUser", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    drive_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
