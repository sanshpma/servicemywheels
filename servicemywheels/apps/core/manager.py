#-*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.utils.crypto import get_random_string


class CustomUserManager(UserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        u = self.create_user(kwargs['email'], password=kwargs['password'])
        u.is_staff = True
        u.save(using=self._db)
        return u

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)