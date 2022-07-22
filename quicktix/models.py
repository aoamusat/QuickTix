from statistics import mode
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Ticket(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    ticket_class = models.CharField(max_length=100)
    departure_date = models.DateField()
    cost = models.IntegerField()
    id_type = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    email = models.EmailField()
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_contact = models.CharField(max_length=100)
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    payment_reference = models.CharField(max_length=100, null = True)
    payment_status = models.CharField(max_length=100, null = True)

    def __str__(self) -> str:
        return f"{self.user.email} <{self.origin} - {self.destination}>"