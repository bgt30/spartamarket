# Generated by Django 4.2 on 2024-12-29 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/user.png', upload_to='profile_images/'),
        ),
    ]
