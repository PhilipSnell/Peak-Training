# Generated by Django 2.2.14 on 2021-05-21 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210521_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingentry',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='trainingentry',
            name='unit',
        ),
        migrations.AlterField(
            model_name='trainingentry',
            name='reps',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='trainingentry',
            name='weight',
            field=models.CharField(max_length=300),
        ),
    ]
