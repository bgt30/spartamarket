# Generated by Django 4.2 on 2024-12-29 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/user.png', null=True, upload_to='profile_images/'),
        ),
    ]
