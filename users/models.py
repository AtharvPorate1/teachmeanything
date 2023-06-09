from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser,grasp_power,comprehension,engagement,learning_speed,curiosity,confidence,background, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        grasp_power=grasp_power,
        comprehension = comprehension ,
        engagement = engagement,
        learning_speed = learning_speed,
        curiosity = curiosity,
        confidence = confidence,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser,
        background = background, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password,grasp_power,comprehension,engagement,learning_speed,curiosity,confidence,background, **extra_fields):
    return self._create_user(email, password, False, False,grasp_power,comprehension,engagement,learning_speed,curiosity,confidence,background, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    grasp_power=models.IntegerField(default=50,validators=[MaxValueValidator(100),MinValueValidator(0)])
    comprehension =models.IntegerField(default=50,validators=[MaxValueValidator(100),MinValueValidator(0)])
    engagement=models.IntegerField(default=50,validators=[MaxValueValidator(100),MinValueValidator(0)])
    learning_speed=models.IntegerField(default=50,validators=[MaxValueValidator(100),MinValueValidator(0)])
    curiosity=models.IntegerField(default=50,validators=[MaxValueValidator(100),MinValueValidator(0)])
    confidence=models.IntegerField(default=50,validators=[MaxValueValidator(100),MinValueValidator(0)])
    background = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name','grasp_power']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)