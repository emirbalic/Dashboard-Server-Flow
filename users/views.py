import logging

from axes.utils import reset
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UsersView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    paginator = None

class OwnUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        # print('OwnUserView is ===================> ', request)
        return Response(serializer.data)

    def put(self, request):
        data = request.data
        print('OwnUserView is ===================> ', request.data)
        if self.checkif_request_field_valid(request, "first_name"):
            request.user.first_name = data["first_name"]
        if self.checkif_request_field_valid(request, "last_name"):
            request.user.last_name = data["last_name"]
        if self.checkif_request_field_valid(request, "email"):
            request.user.email = data["email"]
        request.user.save()
        return Response({}, status=200)

    def checkif_request_field_valid(self, request, field_name):
        if field_name in request.data and request.data[field_name] and request.data[field_name] != "":
            return True
        return False


class NewUserView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request, format=None):
        d = request.data
        user = User(username=d["username"], first_name=d["firstName"],
                    last_name=d["lastName"], email=d["email"], is_staff=d["is_staff"],
                    is_active=True, required_password_change=True, password_change_date=timezone.now())
        user.set_password(d["passwd"])
        status = 201
        try:
            user.save()
        except Exception as e:
            status = 406
            # for error handling
            # return Response({"errors": 'Unique username constraint failed, try with different username'}, status=status)
        return Response({}, status=status)


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request, format=None):
        data = request.data
        user = User.objects.get(id=data["user_id"])
        user.delete()
        return Response({}, status=200)


class ResetUserPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            data = request.data
            new_passwd = data["new_passwd"]
            confirm_passwd = data["confirm_passwd"]

            if (new_passwd != confirm_passwd):
                raise ValidationError(
                    _("Password should match"),
                    code='Password should match'
                )

            validate_password(new_passwd, request.user)
        except ValidationError as e:
            return Response({"errors": e.error_list}, status=403)

        request.user.required_password_change = False
        request.user.password_change_date = timezone.now()
        request.user.set_password(new_passwd)
        request.user.save()

        return Response({"response": "Success"}, status=200)


class AdminResetUserPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request, format=None):
        if not request.user.is_staff:
            return Response({"response": "User is not admin!"}, status=401)

        data = request.data
        new_passwd = data["new_passwd"]
        target_user = data["target_user"]

        validate_password(new_passwd, target_user)

        user = User.objects.get(username=target_user)
        user.required_password_change = False
        user.password_change_date = timezone.now()
        user.set_password(new_passwd)
        user.save()

        return Response({"response": "Success"}, status=200)


class UpdateUserActivityView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request, format=None):
        d = request.data
        username = d["username"]
        activity = d["activity"]

        user = User.objects.get(username=username)
        user.is_active = activity
        user.save()
        return Response({"Activity updated"}, status=200)


class ResetLoginAttemptsView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request, format=None):
        data = request.data
        if 'target_user' not in data.keys():
            raise ValidationError(detail={'target_user': 'This field is required.'})
            # raise exceptions.ValidationError(detail={'target_user': 'This field is required.'})
        if not User.objects.filter(username=data['target_user']).exists():
            raise ValidationError(detail={'target_user': 'Username does not exist.'})
            # raise exceptions.ValidationError(detail={'target_user': 'Username does not exist.'})

        reset(username=data["target_user"])
        return Response({"User unblocked"}, status=200)
