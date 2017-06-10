from django.db import models
import datetime
from decimal import Decimal

from django.contrib.auth.models import User


class MoneyField(models.DecimalField):
    """
    Decimal Field with hardcoded precision of 28 and a scale of 18.
    """

    def __init__(self, verbose_name=None, name=None, max_digits=28,
                 decimal_places=18, **kwargs):
        super(MoneyField, self).__init__(verbose_name, name, max_digits,
                                         decimal_places, **kwargs)


class User(models.Model):
    rehive_identifier = models.CharField(max_length=2000,
                                         unique=True,
                                         blank=False,
                                         null=False)
    created = models.DateTimeField()
    updated = models.DateTimeField()


class Stokvel(models.Model):
    # We are going to create a dummy user on Rehive to act as the stokvel for accounting
    rehive_identifier = models.CharField(max_length=2000,
                                         unique=True,
                                         blank=False,
                                         null=False)
    monthly_payment = MoneyField(default=Decimal(0))
    users = models.ManyToManyField(User)
    description = models.CharField(max_length=255, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()


class Event(models.Model):
    stokvel = models.ForeignKey(Stokvel)
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    payout = MoneyField(default=Decimal(0))
    created = models.DateTimeField()
    updated = models.DateTimeField()


class Vote(models.Model):
    stokvel = models.ForeignKey(Stokvel)
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    updated = models.DateTimeField()