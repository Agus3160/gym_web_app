from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The email is necessary to create an account.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def add_to_group(self, user, group_name):
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        user.save(using=self._db)
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  username = None
  email = models.EmailField(unique=True, blank=False, null=False)
  first_name = models.CharField(max_length=30, blank=False, null=False)
  last_name = models.CharField(max_length=30, blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
  updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  EMAIL_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']


class ClientInfo(models.Model):

    GENDER_LIST = [
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]

    MEMBERSHIP_STATE = [
        ('P','Pending'),
        ('A','Active'),
        ('I','Inactive'),
        ('C','Cancelled'),
    ]

    #Points to the user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #Specific info for clients
    height = models.FloatField(blank=False, null=False)
    weight = models.FloatField(blank=False, null=False,)
    gender = models.CharField(max_length=10, blank=False, null=False, choices=GENDER_LIST)
    birth_date = models.DateField(blank=False, null=False)
    address = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    ci = models.CharField(max_length=255, blank=False, null=False)
    emergency_contact = models.CharField(max_length=255, blank=False, null=False)
    membership_state = models.CharField(max_length=10, default='I',choices=MEMBERSHIP_STATE, blank=False, null=False)
    membership_Type = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

class Services(models.Model):
  name = models.CharField(max_length=255, blank=False, null=False)
  description = models.CharField(max_length=255, blank=False, null=False)
  price = models.FloatField(blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
  updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
