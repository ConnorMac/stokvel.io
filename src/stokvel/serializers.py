import re
import json

# from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from stokvel.models import Stokvel, User, Event, Vote


class RegisterSerializer(serializers.Serializer):
    rehive_identifier = serializers.CharField(required=True)


class StokvelSerializer(serializers.ModelSerializer):
    monthly_payment = serializers.CharField(required=True)
    users = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='email'
     )
    title = serializers.CharField(required=True)
    rehive_identifier = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Stokvel
        fields = ('monthly_payment', 'title', 'users', 'description', 'created', 'updated', 'rehive_identifier',)


class EventSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event

    def create(self, validated_data):
        rehive_user = self.context.get('request').user
        user = User.objects.filter(rehive_identifier=rehive_user['identifier'])
        validated_data['user'] = user
        print(validated_data)
        return super(EventSerializer, self).create(validated_data)


class VoteSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Vote
