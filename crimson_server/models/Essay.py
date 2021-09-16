from django.db import models

class Essay(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    user = models.ForeignKey("CrimsonUser", on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    official_dd = models.DateField()
    floating_dd = models.DateField()
    is_complete = models.BooleanField(default=False)
    notes = models.TextField()
