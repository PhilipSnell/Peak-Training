from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


from django.contrib.postgres.fields import ArrayField


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, confirm_password=None):
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

    def create_superuser(self, email, username, first_name, last_name, password=None):

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

    def create_traineruser(self, email, username, first_name, last_name, password=None, **extra_fields):

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
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_trainer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Trainer(models.Model):
    trainer = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='Trainer')
    clients = models.ManyToManyField(Account, related_name='Clients')

    def __str__(self):

        return self.trainer.email


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
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/', blank=True)
    video = models.URLField()

    def __str__(self):
        return self.name


class TrainingEntry(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='client')
    phase = models.IntegerField()
    week = models.IntegerField()
    day = models.IntegerField()
    reps = models.CharField(max_length=300)
    weight = models.CharField(max_length=300)
    sets = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    exercise = models.ForeignKey(
        ExerciseType, on_delete=models.CASCADE, related_name='Exercise')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['day', 'order']

    def __str__(self):
        return "Phase " + str(self.phase) + " Week " + str(self.week) + " Day " + str(self.day) + " " + str(self.exercise.name)


class SetFeedback(models.Model):
    t_id = models.IntegerField(unique=True)
    comment = models.CharField(max_length=300, blank=True, null=True)
    difficulty = models.IntegerField(null=True)


class Day(models.Model):
    phase = models.IntegerField()
    week = models.IntegerField()
    day = models.IntegerField()
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='DayUser')
    entrys = models.ManyToManyField(TrainingEntry, 'entry', blank=True)

    def __str__(self):
        return "Phase " + str(self.phase) + " Week " + str(self.week) + " Day " + str(self.day)


class Week(models.Model):
    phase = models.IntegerField()
    week = models.IntegerField()
    days = models.ManyToManyField(Day, 'days', blank=True)
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='WeekUser')
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return "Phase " + str(self.phase) + " Week " + str(self.week)


class Phase(models.Model):
    phase = models.IntegerField()
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='PhaseUser')
    weeks = models.ManyToManyField(Week, related_name='weeks', blank=True)

    def __str__(self):
        return "Phase "+str(self.phase)


class Message(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('-timestamp',)

# class DailyTracking(models.Model):
#
#     client = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='DTclient')
#     date = models.DateField()

# Todo add group of tracking field manytomany


class TrackingTextValue(models.Model):
    value = models.CharField(max_length=30)
    client = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='textFieldClient')
    date = models.DateField()
    field_id = models.IntegerField()


class TrackingTextField(models.Model):
    name = models.CharField(max_length=30)
    clientToggle = models.ManyToManyField(Account, blank=True, default=None)
    values = models.ManyToManyField(TrackingTextValue, blank=True)
    type = models.BooleanField()  # False if text field, True if integer only field


class TrackingGroup(models.Model):
    trainer = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='groupTrainer')
    name = models.CharField(max_length=30)
    clientToggle = models.ManyToManyField(
        Account, blank=True, default=None, related_name='clientToggle')
    textfields = models.ManyToManyField(
        TrackingTextField, related_name='textfield', blank=True)


# class ClientConfig(models.Model):
#     client = models.OneToOneField(Account, on_delete=models.CASCADE)
#     groups = models.ManyToManyField(TrackingGroup, related_name='trackinggroup', blank=True)

# Create your models here.
