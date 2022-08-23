from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ForgotPasswordView, LoginView, LogoutAPIView, NewPasswordView, RegisterAPIView, activate, email_sending

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('password_confirm/<str:activation_code>', NewPasswordView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('send_email/', email_sending)
]