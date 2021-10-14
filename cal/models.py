from django.db import models

class Event(models.Model):
    start_time = models.DateTimeField
    end_time = models.DateTimeField
    duration = models.DurationField
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)


# Create your models here.
