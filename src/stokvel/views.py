from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, CursorPagination

from stokvel.serializers import RegisterSerializer, StokvelSerializer, EventSerializer, VoteSerializer

from rehive import Rehive, APIException
from stokvel.authentication import ValidateWithRehive
from stokvel.permissions import UserPermission

from stokvel.models import User, Stokvel
from django.utils import timezone

from random import randint


class ResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

        return Response(OrderedDict([('status', 'success'), ('data', response)]))


class LargeResultsSetPagination(CursorPagination):
    page_size = 50
    cursor_query_param = 'cursor'
    max_page_size = 500

    def get_paginated_response(self, data):
        response = OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

        return Response(OrderedDict([('status', 'success'), ('data', response)]))


class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class ListModelMixin(object):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'data': serializer.data})


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'status': 'success', 'data': serializer.data})


class UpdateModelMixin(object):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'status': 'success', 'data': serializer.data})

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(serializer)
        return Response(
            data={'status': 'success'},
            status=status.HTTP_200_OK)

    def perform_destroy(self, serializer):
        serializer.destroy()


class CreateAPIView(CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ListCreateAPIView(ListModelMixin,
                        CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(RetrieveModelMixin,
                            UpdateModelMixin,
                            GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating, deleting model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveAPIView(RetrieveModelMixin,
                      GenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['company'] = 'stokvel_io'

        rehive = Rehive()
        try:
            response = rehive.auth.register(data)
            user = User(
                rehive_identifier=response['data']['user']['identifier'],
                email=response['data']['user']['email'],
                created=timezone.now(),
                updated=timezone.now()
            )
            user.save()
        except APIException as e:
            return Response(
                e.data,
                status=e.status
            )

        return Response(
            response,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['company'] = 'stokvel_io'
        RehiveSDK = Rehive()
        response = RehiveSDK.auth.login(data)

        return Response(
                response,
                status=status.HTTP_200_OK
            )


class StokvelView(ListCreateAPIView):
    authentication_classes = (ValidateWithRehive,)
    permission_classes = (UserPermission,)
    serializer_class = StokvelSerializer

    def post(self, request, *args, **kwargs):
        # Disgusting hacks that need to be fixed
        rehive = Rehive()

        email_append = randint(1, 9999)
        stokvel_user_data = {
            'email': 'stokvel+' + str(email_append) + '@rehive.com',
            'first_name': 'stokvel',
            'last_name': 'stokvel',
            'company': 'stokvel_io',
            'password1': 'fT!3<5,n<-<P9d5',
            'password2': 'fT!3<5,n<-<P9d5'
        }
        try:
            response = rehive.auth.register(stokvel_user_data)
            data = response.get('data')
            mutable = request.data._mutable
            request.data._mutable = True
            request.data['rehive_identifier'] = data.get('user').get('identifier')
            request.data._mutable = mutable
            return super(StokvelView, self).post(request, *args, **kwargs)
        else APIException as e:
            return Response(
                e.data,
                status=e.status
            )

    def perform_create(self, serializer):
        serializer.save(users=User.objects.filter(email__in=self.request.data['users']))


class EventView(ListCreateAPIView):
    authentication_classes = (ValidateWithRehive,)
    permission_classes = (UserPermission,)
    serializer_class = EventSerializer


class VoteView(ListCreateAPIView):
    authentication_classes = (ValidateWithRehive,)
    permission_classes = (UserPermission,)
    serializer_class = VoteSerializer

