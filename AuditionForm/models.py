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
    phone = models.IntegerField(max_length=10, null=True)
    department = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=30, null=True)
    domain = models.JSONField(default=list, null=True, blank=True)  # Store serialized JSON
    questions_answers = models.JSONField(default=dict, blank=True, null=True)
    # questions_answers2 = models.JSONField(default=dict, blank=True, null=True)
    # desc = models.CharField(max_length=200, null=True, unique=False)


    def __str__(self):
        return self.name
