from crimson_server.models.Student import Student
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from crimson_server.models import Student

class Essay(models.Model):
    student = models.ForeignKey(Student, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    official_dd = models.DateField()
    floating_dd = models.DateField()
    is_complete = models.BooleanField(default=False)
    notes = models.TextField()
