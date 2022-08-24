from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import *
from .serializers import *


User = get_user_model()

class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Account created')

@api_view(["GET"])
def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect("http://127.0.0.1:3000/")


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            {"msg":"You successfully logged out"}, 
            status=status.HTTP_204_NO_CONTENT
        )

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotSerializer)
    def post(self, request):
        data = request.POST
        serializer = ForgotSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = "Please, confirm your email"
            return Response(message)

class NewPasswordView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        new_password = user.generate_activation_code()
        user.set_password(new_password)
        user.save()
        return Response(f"Your new password is {new_password}")

@api_view(["GET"])
def email_sending(request):
    user = User.objects.get(email="elabdrasulov@gmail.com")
    user.send_activation_code()
    return Response('Check your email and activate your account')

@api_view(["GET"])
def password_confirmation(request):
    user = User.objects.get(email="elabdrasulov@gmail.com")
    user.password_confirm()
    return Response('Check your email for password changes')

class UserFollowingView(CreateAPIView, DestroyAPIView):

    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = [IsAuthenticated, IsAuthor, ]

    def post(self, request):
        user = request.user
        follow = User.objects.get(id=request.data.get('following_user_id'))

        if UserFollowing.objects.filter(user_id=user, following_user_id=follow).exists():
            UserFollowing.objects.get(user_id=user, following_user_id=follow).delete()
            return Response("Unfollowed")
        else:
            UserFollowing.objects.create(user_id=user, following_user_id=follow)
            return Response("Followed")

class UserFollowerView(CreateAPIView, DestroyAPIView):

    queryset = UserFollowing.objects.all()
    serializer_class = FollowersSerializer
    permission_classes = [IsAuthenticated, IsAuthor, ]

class ProfileView(ListAPIView):

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

class ProfileDetailView(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# class AddFollower(APIView):
#     permission_classes = [IsAuthenticated, ]
#     def post(self, request):
#         user = User.objects.get(user_id=self.request.data.get('user_id'))
#         follow = User.objects.get(user_id=self.request.data.get('follow'))

#         if UserFollowing.objects.filter(user_id=user.id, following_user_id=follow.id).exists():
#             UserFollowing.objects.get(user_id=user.id, following_user_id=follow.id).delete()
#             return Response("Unfollowed")
#         else:
#             UserFollowing.objects.create(user_id=user.id, following_user_id=follow.id)
#             return Response("Followed")

        
# @api_view(["POST"])
# def to_follow(request, user_id):
#     if UserFollowing.objects.filter(user_id=request.user.id, following_user_id=User.objects.get(id=user_id)).exists():
#         UserFollowing.objects.get(user_id=request.user.id, following_user_id=User.objects.get(id=user_id)).delete()
#         return Response("Unfollowed")
#     else:
#         UserFollowing.objects.create(user_id=request.user.id, following_user_id=User.objects.get(id=user_id))
#         return Response("Followed")

# UserFollowing.objects.create(user_id=user.id,
#                             following_user_id=follow.id)

# @api_view(["GET"])
# def profile_view(request, user=None):
#     if user is None:
#         user = request.user
#     else:
#         user = get_object_or_404(User, email=user)

#     follow = user.following.all().count()
#     followers = UserFollowing.objects.filter(following_user_id=user).count()
#     videos = user.posts.all()
#     return Response()

# user = get_object_or_404(User, email=email)

# videos = user.posts.all()
