import re

# from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    rehive_identifier = serializers.CharField(required=True)
    