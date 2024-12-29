from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

def validate_hashtag(value):
    if ' ' in value or not re.match("^[a-zA-Z0-9_]+$", value):
        raise ValidationError('해시태그는 띄어쓰기와 특수문자를 포함할 수 없습니다.')

class Hashtag(models.Model):
    name = models.CharField(
        max_length=50, 
        unique=True,
        validators=[validate_hashtag]
    )

    def __str__(self):
        return f'#{self.name}'

    def clean(self):
        self.name = self.name.lower()  # 해시태그를 소문자로 저장

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_products')
    likes = models.ManyToManyField(User, related_name='liked_products', blank=True)
    view_count = models.IntegerField(default=0)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='products')

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

