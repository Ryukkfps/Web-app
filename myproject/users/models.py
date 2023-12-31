from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




# class CustomAccountManager(BaseUserManager):
    
#     def create_superuser(self, email, user_name, first_name, password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_staff=True'
#             )
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_superuser=True'
#             )
        
#         return self.create_user(email, user_name, first_name, password, **other_fields)


    
    
#     def create_user(self, email, user_name, first_name, password, **other_fields):
#         if not email:
#             raise ValueError(_('You must provide an email address'))
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, user_name= user_name, first_name=first_name, **other_fields)
#         user.set_password(password)
#         user.save()

#         return user

# class NewUser(AbstractBaseUser, PermissionsMixin):

#     email = models.EmailField(_('email address'), unique = True)
#     user_name = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=100, blank=True)
#     start_date = models.DateTimeField(default=timezone.now)
#     about = models.TextField(_('about'),max_length=500,blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#     can_view_process = models.BooleanField(default=False)

#     objects = CustomAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['user_name','first_name']

#     def __str__(self):
#         return self.user_name