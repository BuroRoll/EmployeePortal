from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login, name, password, **extra_fields):
        values = [login, name]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        user = self.model(
            login=login,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, name, password, **extra_fields)

    def create_superuser(self, login, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(login, name, password, **extra_fields)


class Position(models.Model):
    position_name = models.CharField(max_length=100)
    access_to_candidates = models.BooleanField(default=False)
    access_to_vacation_list = models.BooleanField(default=False)

    def __str__(self):
        return self.position_name


class Account(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=250)
    info = models.TextField(blank=True)
    phone = models.CharField(max_length=50)
    vacation_days = models.TextField(blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, default='users/default_profile_pic.png')
    slack_login = models.CharField(max_length=40, blank=True)
    telegram_login = models.CharField(max_length=40, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    is_new_employee = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'phone']


class Candidate(models.Model):
    name = models.CharField(max_length=250)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
