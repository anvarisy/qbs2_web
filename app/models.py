from django.db import models
from django.contrib.auth.models  import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # return 'user_{0}/{1}'.format(instance.user.email, filename)
    # return '{0}/{1}'.format(instance.album.album_name, filename)
    case_name = instance.user.email
    file_name = filename.lower().replace(" ", "_")
    return "Users/{}/{}".format(case_name, file_name)

class user(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=160, blank=True)
    mobile_number = models.CharField(max_length=13,blank=True)
    is_admin = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    kadiv = models.ForeignKey('self',blank=True, null=True, on_delete=models.CASCADE)
    objects = UserManager()
    date_joined = models.DateTimeField(default=timezone.now)
    user_photo = models.ImageField(upload_to=user_directory_path, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of teacher?"
        # Simplest possible answer: All admins are teacher
        return self.is_admin
