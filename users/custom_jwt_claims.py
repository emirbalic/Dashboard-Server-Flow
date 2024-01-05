from datetime import timedelta, timezone

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import Token

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import exceptions

#django axes imports
from django.dispatch import receiver
from axes.signals import user_locked_out
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone

from django.conf import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

# #32.29 == https://www.youtube.com/watch?v=xjMP0hspNLE
# # in case I need a username from token in frontend
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        user_logged_in.send(sender=self.user.__class__, request=self.context['request'], user=self.user)
        # print('user_logged_in ------ >', user_logged_in)
        refresh = self.get_token(self.user)

        diff = (timezone.now() - self.user.password_change_date)
        time_diff = diff.days
        if(time_diff >= 90): #to test I'll have just one
        # if(time_diff >= settings.PASSWORD_EXPIRATION_TIME):
            self.user.required_password_change=True
            self.user.save()

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra json fields
        data['is_admin'] = self.user.is_staff
        data['is_active'] = self.user.is_active
        data['requires_reset'] = self.user.required_password_change
        data['username'] = self.user.username
        data['id'] = self.user.id
        # print('data here :::::  ------ >', data)
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # print('whats happening here? - ', request)
        try:
            response = super().post(request, *args, **kwargs)
            # print('response try===================> ', response)
        except exceptions.AuthenticationFailed as e:
            if getattr(request, "axes_locked_out", request):
                print('response except===================> ', request)
                raise exceptions.AuthenticationFailed(detail='Due to the too many unsuccessfull attempts your account is blocked. Please contact the administrator of the system.')
            else:
                raise e
        return response


class IndefiniteAccessToken(Token):
    token_type = 'access'
    lifetime = timedelta(weeks=9999)
