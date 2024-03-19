from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, BaseUserManager
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


class User(AbstractBaseUser):
  username = None
  email = models.EmailField(unique=True, blank=False, null=False)
  first_name = models.CharField(max_length=30, blank=False, null=False)
  last_name = models.CharField(max_length=30, blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
  updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

  USERNAME_FIELD = 'email'