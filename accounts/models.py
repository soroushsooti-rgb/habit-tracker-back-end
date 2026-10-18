from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """ساخت و ذخیره یک کاربر عادی"""
        if not email:
            raise ValueError('ایمیل حتماً باید وارد شود.')


        email = self.normalize_email(email)


        user = self.model(email=email, name=name, **extra_fields)


        user.set_password(password)


        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """ساخت و ذخیره سوپریوزر (ادمین)"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپریوزر حتماً باید is_staff=True داشته باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'سوپریوزر حتماً باید is_superuser=True داشته باشد.')

        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


    def __str__(self):
        return self.email
