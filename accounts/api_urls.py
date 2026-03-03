from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/register/', api_views.RegisterView.as_view(), name='api_register'),
    path('auth/login/', api_views.LoginView.as_view(), name='api_login'),
    path('auth/logout/', api_views.LogoutView.as_view(), name='api_logout'),
    path('auth/profile/', api_views.ProfileView.as_view(), name='api_profile'),
    path('auth/change-password/', api_views.ChangePasswordView.as_view(), name='api_change_password'),
    path('auth/token/refresh/', api_views.TokenRefreshAPIView.as_view(), name='api_token_refresh'),
]
