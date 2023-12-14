from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView
    # , TokenVerifyView,
)
from .custom_jwt_claims import CustomTokenObtainPairView

from users.views import UsersView, NewUserView, DeleteUserView, ResetUserPasswordView, UpdateUserActivityView, \
    AdminResetUserPasswordView, ResetLoginAttemptsView, OwnUserView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UsersView)

urlpatterns = [
    path('', include(router.urls)),
    path('users/me', OwnUserView.as_view(), name='own_user'),
    path('users/new', NewUserView.as_view(), name='new_user'),
    path('users/delete', DeleteUserView.as_view(), name='delete_user'),
    path('users/user-reset-password', ResetUserPasswordView.as_view(), name='reset_password'),
    path('users/admin-reset-password', AdminResetUserPasswordView.as_view(), name='admin_reset_password'),
    path('users/admin-reset-login-attempts', ResetLoginAttemptsView.as_view(), name='admin_reset_login_attempts'),
    path('users/update-activity', UpdateUserActivityView.as_view(), name='update_activity'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
