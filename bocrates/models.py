from email.policy import default
import imp
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
import datetime

class Rate(models.Model):
    name = models.CharField(max_length=300)
    interestRate = models.FloatField(max_length=10)
    date = models.DateField(datetime.date.today())
    financialMarket = models.CharField(max_length=300)
