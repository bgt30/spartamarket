from django import forms
from .models import Product, Hashtag
import re

class ProductForm(forms.ModelForm):
    hashtags = forms.CharField(
        required=False,
        help_text='쉼표로 구분하여 입력해주세요 (예: tag1,tag2,tag3)'
    )

    class Meta:
        model = Product
        fields = ('title', 'description')

    def clean_hashtags(self):
        hashtags = self.cleaned_data.get('hashtags', '')
        if hashtags:
            tags = [tag.strip().lower() for tag in hashtags.split(',') if tag.strip()]
            for tag in tags:
                if ' ' in tag or not re.match("^[a-zA-Z0-9_]+$", tag):
                    raise forms.ValidationError('해시태그는 띄어쓰기와 특수문자를 포함할 수 없습니다.')
            return hashtags
        return ''
