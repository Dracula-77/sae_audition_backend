from django.db import models
import json

class AuditionData(models.Model):
    domains_choices = [
        ('Event Management', 'Event Management'),
        ("Automobiles", "Automobiles"),
        ("Robotics", "Robotics"),
        ("Web Development", "Web Development"),
        ("Graphics Designing", "Graphics Designing"),
    ]
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    roll = models.CharField(max_length=10, null=True, unique=True)
    domain = models.JSONField(default=list, null=True, blank=True)  # Store serialized JSON
    desc = models.CharField(max_length=200, null=True, unique=False)


    def __str__(self):
        return self.name
