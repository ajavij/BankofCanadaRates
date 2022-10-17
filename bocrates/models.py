import datetime
from email.policy import default
from django.db import models


class Rate(models.Model):
    InterestRate = models.FloatField(max_length=10, null=True)
    Date = models.DateField(datetime.date.today())
    FinancialMarket = models.CharField(max_length=300)
