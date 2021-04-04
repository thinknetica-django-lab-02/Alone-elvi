from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    """Класс ProfileForm отвечает за отображение формы редактирования своего профиля"""
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
