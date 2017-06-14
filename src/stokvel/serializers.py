import re
import json

# from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from stokvel.models import Stokvel, User


class RegisterSerializer(serializers.Serializer):
    rehive_identifier = serializers.CharField(required=True)


class StokvelSerializer(serializers.ModelSerializer):
    monthly_payment = serializers.CharField(required=True)
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    title = serializers.CharField(required=True)
    rehive_identifier = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Stokvel
        fields = ('monthly_payment', 'title', 'users', 'description', 'created', 'updated', 'rehive_identifier',)

