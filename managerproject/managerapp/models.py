#Local Imports
import uuid

#Django Local Imports
from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
)

class UpdatedUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """

        if not username:
            username = str(uuid.uuid4())
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username, email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username,
                    email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            username, email, password, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
    
        username = None

        return self._create_user(
            username, email, password, **extra_fields
        )

class User(AbstractUser):
    email = models.EmailField(_("Email_ID"), max_length=255,unique=True)
    password = models.CharField(_("Password"), max_length=1000)
    username = models.CharField(_("Username"), max_length=50,null=True,blank=True)

    objects = UpdatedUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"