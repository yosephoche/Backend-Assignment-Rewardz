import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from authentication.managers import UserBookManager
from library_system.behaviors import Timestampable


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        account = self.model(
            email=self.normalize_email(kwargs.get('email')),
            username=kwargs.get('email')
        )

        account.set_password(kwargs.get('password'))
        account.save()

        return account

    def create_superuser(self, **kwargs):
        account = self.create_user(**kwargs)
        account.is_staff = True
        account.is_superuser = True
        account.is_active = True
        account.save()

        return account


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_STUDENT = 'student'
    ROLE_LIBRARIAN = 'librarian'
    USER_ROLE = (
        (ROLE_STUDENT, 1),
        (ROLE_LIBRARIAN, 2),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=500)

    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    unique_id = models.CharField(max_length=500, default=uuid.uuid4, editable=False, unique=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, choices=USER_ROLE, default=ROLE_STUDENT)
    admin_panel_access = models.BooleanField(default=False)

    verify = models.BooleanField(default=True)

    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    # company_list = ArrayField(models.IntegerField(null=True, default=None), size=10)
    objects = UserManager()
    user_books = UserBookManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_fullname(self):
        return '%s %s' % (self.first_name, self.last_name)


class UserAwareModel(Timestampable, models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
