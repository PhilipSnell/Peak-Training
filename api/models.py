from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.postgres.fields import ArrayField

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username, first_name, last_name,password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email,username, first_name, last_name,password=None):

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            )
        user.is_admin = True
        user.is_trainer = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def create_traineruser(self,email,username, first_name, last_name,password=None, **extra_fields):

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            )
        user.is_admin = False
        user.is_trainer = True
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique= True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_trainer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()
    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True
class Trainer(models.Model):
    trainer = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='Trainer')
    clients = models.ManyToManyField(Account, related_name='Clients')

class Set_Entry(models.Model):
    t_id = models.IntegerField(unique=True)
    sets = models.IntegerField()
    reps = models.CharField(max_length=300)
    weights = models.CharField(max_length=300)
    e_id = models.IntegerField()

    def __str__(self):
        exercise = ExerciseType.objects.get(id=self.e_id)
        return exercise.name



class ExerciseType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/', blank=True)
    video = models.URLField()

    def __str__(self):
        return self.name


class TrainingEntry(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='User')
    phase = models.IntegerField()
    week = models.IntegerField()
    day = models.IntegerField()
    reps = models.CharField(max_length=300)
    weight = models.CharField(max_length=300)
    sets = models.IntegerField()
    exercise = models.ForeignKey(ExerciseType, on_delete=models.CASCADE, related_name='Exercise')


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('-timestamp',)
# Create your models here.
