from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from stokvel.serializers import RegisterSerializer

from stokvel.rehive.rehive import Rehive

from stokvel.models import User
from django.utils import timezone


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data
        RehiveSDK = Rehive()
        response = RehiveSDK.register(data)
        
        if response['data']['user']['identifier'] is not None:
            user = User(
                rehive_identifier=response['data']['user']['identifier'],
                created=timezone.now(),
                updated=timezone.now()
            )
            user.save()

        return Response(
            response,
            status=status.HTTP_201_CREATED
        )
