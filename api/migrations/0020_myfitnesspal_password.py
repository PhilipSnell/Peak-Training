# Generated by Django 2.2.14 on 2022-06-14 19:28

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_myfitnesspal_connected'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfitnesspal',
            name='password',
            field=encrypted_model_fields.fields.EncryptedCharField(default=2),
            preserve_default=False,
        ),
    ]