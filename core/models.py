from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from taggit.managers import TaggableManager

import uuid
# Authentication and Authorization

PRODUCT_TYPE_CHOICES = [
    ('Module', 'Module'),
    ('Inverter', 'Inverter'),
    ('Battery', 'Battery')
]

# Create an auth token every time a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email_address, password, **extra_fields):
        if not email_address:
            raise ValueError('The given email_address must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email_address, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email_address, password, **extra_fields)

    def create_superuser(self, email_address, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email_address, password, **extra_fields)


class User(AbstractBaseUser):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_address = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # FK one to many
    # entity = models.ForeignKey(Entity, on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email_address'
    EMAIL_FIELD = 'email_address'

    def __str__(self):
        return self.email_address

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, core):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser

    tags = TaggableManager()


class Product(models.Model):
    ProductCode = models.CharField(max_length=45, primary_key=True)
    Description = models.TextField( null=True,blank=True)
    ManufacturerName = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerProductID = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerCode = models.CharField(blank=True, null=True, max_length=6)
    ProductType = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=75)


class Manufacturer(models.Model):
    ManufacturerCode = models.CharField(unique=True, max_length=6)
    ManufacturerName = models.CharField(unique=True, max_length=75)
    LegalEntityIdentifier = models.CharField(unique=True, max_length=75)


class Module(models.Model):
    ProductCode = models.CharField(max_length=75, primary_key=True)
    Description = models.TextField( null=True,blank=True)
    ManufacturerName = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerProductID = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerCode = models.CharField(blank=True, null=True, max_length=6)
    ProductType = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=75)
    ModuleTechnology = models.CharField(blank=True, null=True, max_length=75)
    ModuleNameplateCapacity = models.CharField(blank=True, null=True, max_length=75)
    FrameColor = models.CharField(blank=True, null=True, max_length=75)
    BacksheetColor = models.CharField(blank=True, null=True, max_length=75)
    Bifacial = models.BooleanField(blank=True, null=True)


class Inverter(models.Model):
    ProductCode = models.CharField(max_length=75, primary_key=True)
    Description = models.TextField( null=True,blank=True)
    ManufacturerName = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerProductID = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerCode = models.CharField(blank=True, null=True, max_length=6)
    ProductType = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=75)
    Power = models.CharField(blank=True, null=True, max_length=75)
    Phases = models.CharField(blank=True, null=True, max_length=75)
    Transformerless = models.BooleanField(blank=True, null=True)


class Battery(models.Model):
    ProductCode = models.CharField(max_length=35, primary_key=True)
    Description = models.TextField( null=True,blank=True)
    ManufacturerName = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerProductID = models.CharField(blank=True, null=True, max_length=75)
    ManufacturerCode = models.CharField(blank=True, null=True, max_length=6)
    ProductType = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=75)


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name



