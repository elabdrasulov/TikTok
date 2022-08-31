from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from .views import ChangePasswordView, ForgotPasswordView, LoginView, LogoutAPIView, NewPasswordView, ProfileDetailView, ProfileView, RegisterAPIView, UserFollowerView, UserFollowingView, activate
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('password_confirm/<str:activation_code>/', NewPasswordView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('profile/', MyProfileView.as_view()),
    path('profiles/', ProfileView.as_view()),
    path('profile/<int:pk>/', ProfileDetailView.as_view()),
    path('profile/follow/', UserFollowingView.as_view()),
    # path('profile/follow/', AddFollower.as_view()),
    # path('profile/to_follow/<int:user_id>/', to_follow)
    # path('profile/followers/', UserFollowerView.as_view()),
]