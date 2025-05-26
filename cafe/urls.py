from django.urls import path
from .views import ProtectedView, LogoutView, RegisterAPI, register_page, index
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

urlpatterns = [
    path('index/', index, name="homepage"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login-page'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_cafe'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('register/', register_page, name='register-page'),
    path('api/register/', RegisterAPI.as_view(), name='register-api'),
]