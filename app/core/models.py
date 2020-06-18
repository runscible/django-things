from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin  

class UserManager(BaseUserManager):

    def create_user(self , email, password=None, **extra_fields):
        """ create new custom user """
        if not email:
          raise ValueError('email is required for create users')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
      """ creates a new super user """
      user = self.create_user(email, password)
      user.is_staff = True
      user.is_superuser = True
      user.save(using=self._db)
      
      return user


class User(AbstractBaseUser, PermissionsMixin):
  """ custom user model that supports using email instead of username for login """
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True) 
  is_staff = models.BooleanField(default=False) 

  objects = UserManager()

  USERNAME_FIELD = 'email'

class Tag(models.Model):
  """tags for recipe"""
  name=models.CharField(max_length=255)
  user=models.name = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return self.name
  
    