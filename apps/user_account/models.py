from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

# from .utils import send_activation_code, password_confirm


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def generate_random_password():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code 

    def create_user(self, email, password=None, **extra_fields):

        # if not email:
        #     raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password==None:
            # password = self.make_random_password()
            user.set_password(password)
            user.is_active = True
            user.save(using=self._db)
        else:
            user.set_password(password)
            user.is_active = False
            user.save(using=self._db)
            user.save()
        # user.set_password(password)

        # user.set_password(password)
        # user.is_active = False
        # user.save(using=self._db)

        # if not password:
        #     password = self.generate_random_password()
        #     user.set_password(password)
        #     user.is_active = True
        #     user.save(using=self._db)

        # else:
        #     user.set_password(password)
        #     user.is_active = False
        #     user.save(using=self._db)

        # if user.password == '12345':
        #     user.is_active = True
        #     # user.save(using=self._db)
        #     user.save()
        # else:
        #     user.is_active = False
        #     user.save(using=self._db)
    
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user
    
AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    name = models.CharField(verbose_name="Name", max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='users', blank=True, null=True)
    activation_code = models.CharField(max_length=8, blank=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]

    objects = CustomUserManager()

    @staticmethod
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code 

    def set_activation_code(self):
        code = self.generate_activation_code()
        if User.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()

    # def send_activation_code(self):
    #     send_activation_code.delay(self.id)
        
    # def password_confirm(self):
    #     password_confirm.delay(self.id)

    def send_activation_code(self):
        self.generate_activation_code()
        self.set_activation_code()
        # activation_url = f'http://127.0.0.1:8000/user_account/activate/{self.activation_code}'
        activation_url = f'https://tektonik.herokuapp.com/user_account/activate/{self.activation_code}'
        message = f'Activate your account, following this link {activation_url}'
        send_mail("Activate account", message, "tiktok@gmail.com", [self.email, ])

    def password_confirm(self):
        # activation_url = f'http://127.0.0.1:8000/user_account/password_confirm/{self.activation_code}'
        activation_url = f'https://tektonik.herokuapp.com/user_account/password_confirm/{self.activation_code}'
        message = f"""
        Do you want to change password?
        Confirm password changes: {activation_url}
        """
        send_mail("Please confirm your new changes", message, "tiktok@gmail.com", [self.email, ])


    def __str__(self) -> str:
        return f'{self.username} -> {self.email}'
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"