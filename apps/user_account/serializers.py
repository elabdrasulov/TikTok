from dataclasses import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.video.serializers import PostSerializer

from .models import *
from .utils import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password',
            'password_confirm' 
        ]
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        return email

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        return attrs

    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        user.set_activation_code()
        user.send_activation_code()

    # def save(self):
    #     data = self.validated_data
    #     user = User.objects.create_user(**data)
    #     user.send_activation_code()

class ForgotSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Such email does not found')
        return attrs
    
    def save(self):
        data = self.validated_data
        user = User.objects.get(**data)
        user.set_activation_code()
        user.password_confirm()

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, min_length=8, write_only=True
    )

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist')
        return email

    def validate (self, attrs):
        email = attrs.get('email', )
        password = attrs.pop('password', )
        filtered_user_by_email = User.objects.filter(email=email)
        # user = auth.authenticate(email=email, password=password)
        user = User.objects.get(email=email)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')

        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh']=str(refresh)
            attrs['access']=str(refresh.access_token)

        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class FollowingSerializer(serializers.ModelSerializer):
    following_user_image = serializers.ImageField(source='following_user_id.image', required=False)

    class Meta:
        model = UserFollowing
        fields = [
            "id", 
            "following_user_id", 
            "following_user_image",
            "created", 
        ]
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['following_username'] = instance.following_user_id.username
        return rep

class FollowersSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user_id.image', required=False)

    class Meta:
        model = UserFollowing
        fields = [
            "id", 
            "user_id",
            "user_image",
            "created",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = instance.user_id.username
        return rep

class ProfileSerializer(serializers.ModelSerializer):

    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    follows_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "image",
            "following",
            "followers",
            "follows_count",
            "followers_count",
        )

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data

    def get_follows_count(self, obj):
        return obj.following.all().count()

    def get_followers_count(self, obj):
        return obj.followers.all().count()


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'