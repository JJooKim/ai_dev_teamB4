from django import forms

from .models import Youtube # 모델 호출

class YoutubeForm(forms.ModelForm):
    class Meta:
        model = Youtube
        fields = ('url',)