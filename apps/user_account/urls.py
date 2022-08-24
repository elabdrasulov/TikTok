from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ForgotPasswordView, LoginView, LogoutAPIView, NewPasswordView, ProfileDetailView, ProfileView, RegisterAPIView, UserFollowerView, UserFollowingView, activate, email_sending, password_confirmation


# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register("follow", )


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('password_confirm/<str:activation_code>', NewPasswordView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('send_email/', email_sending),
    path('send_new_password/', password_confirmation),
    path('profile/', ProfileView.as_view()),
    path('profile/<int:pk>/', ProfileDetailView.as_view()),
    path('profile/follow/', UserFollowingView.as_view()),
    # path('profile/follow/', AddFollower.as_view()),
    # path('profile/to_follow/<int:user_id>/', to_follow)
    # path('profile/followers/', UserFollowerView.as_view()),
]