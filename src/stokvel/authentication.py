import requests
import json

from rest_framework import authentication, exceptions
from stokvel.rehive.rehive import Rehive
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from stokvel.models import User


class ValidateWithRehive(authentication.BaseAuthentication):

    def authenticate(self, request):
        try:
            token = self.get_token_value(request)
            RehiveSDK = Rehive(token)
            response = RehiveSDK.get_current_user()

            if response['http_code'] == 200:
                user = response['data']
                try:
                    stokvel_user = User.objects.get(
                        rehive_identifier=user['identifier'])
                except User.DoesNotExist:
                    raise exceptions.AuthenticationFailed(
                        _('Invalid Stokvel user'))

            else:
                raise exceptions.AuthenticationFailed(_('Invalid user'))

        except Exception as e:
            raise exceptions.AuthenticationFailed('Authentication error.')
        
        # stokvel_user.info = True
        return user, token

    @staticmethod
    def get_token_value(request):
        try:
            auth = request.META['HTTP_AUTHORIZATION'].split()
        except KeyError:
            return None

        if not auth or smart_text(auth[0].lower()) != "token":
            return None

        if not auth[1]:
            return None

        return auth[1]