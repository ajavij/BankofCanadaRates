from django.db import models

class Rate(models.Model):
    name = models.CharField(max_length=300)
    interestRate = models.FloatField(max_length=5)
