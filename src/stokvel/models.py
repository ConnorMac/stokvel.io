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
    email = models.CharField(max_length=255,
                             unique=True,
                             blank=False,
                             null=False)
    rehive_identifier = models.CharField(max_length=2000,
                                         unique=True,
                                         blank=False,
                                         null=False)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class Stokvel(models.Model):
    # We are going to create a dummy user on Rehive to act as the stokvel for accounting
    rehive_identifier = models.CharField(max_length=2000,
                                         unique=True,
                                         blank=False,
                                         null=False)
    monthly_payment = MoneyField(default=Decimal(0))
    users = models.ManyToManyField(User)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now()

        self.updated = datetime.datetime.now()
        return super(Stokvel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    stokvel = models.ForeignKey(Stokvel)
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    payout = MoneyField(default=Decimal(0))
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now()

        self.updated = datetime.datetime.now()
        return super(Event, self).save(*args, **kwargs)


class Vote(models.Model):
    stokvel = models.ForeignKey(Stokvel)
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now()

        self.updated = datetime.datetime.now()
        return super(Vote, self).save(*args, **kwargs)