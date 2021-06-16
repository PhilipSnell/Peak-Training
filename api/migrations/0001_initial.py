# Generated by Django 2.2.14 on 2021-06-14 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_trainer', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('video', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Set_Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_id', models.IntegerField(unique=True)),
                ('sets', models.IntegerField()),
                ('reps', models.CharField(max_length=300)),
                ('weights', models.CharField(max_length=300)),
                ('e_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('days', models.ManyToManyField(blank=True, related_name='days', to='api.Day')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.CharField(max_length=300)),
                ('weight', models.CharField(max_length=300)),
                ('sets', models.IntegerField()),
                ('comment', models.CharField(blank=True, max_length=300)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Exercise', to='api.ExerciseType')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clients', models.ManyToManyField(related_name='Clients', to=settings.AUTH_USER_MODEL)),
                ('trainer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Trainer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL)),
                ('weeks', models.ManyToManyField(blank=True, related_name='weeks', to='api.Week')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.AddField(
            model_name='day',
            name='entrys',
            field=models.ManyToManyField(blank=True, related_name='entry', to='api.TrainingEntry'),
        ),
    ]
