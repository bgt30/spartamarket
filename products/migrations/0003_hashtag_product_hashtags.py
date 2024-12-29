# Generated by Django 4.2 on 2024-12-29 06:13

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_view_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[products.models.validate_hashtag])),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.hashtag'),
        ),
    ]