from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model"""

    def create_user(self, email, name, password=None):
        """Creates a custom user profile"""

        if not email:
            raise ValueError('User must have a valid email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates a custom Superuser Profile"""

        user = self.create_user(email=email, name= name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Class for Custom UserProfile that extends the functionality of Django Built in User Profile"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Gives the full name of the user object"""

        return self.name

    def __str__(self):
        """Provides the string representation of the object"""

        return self.email


