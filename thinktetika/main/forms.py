from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


ProfileForm = forms.inlineformset_factory(User, Profile, fields=('birth_date', 'avatar',), extra=0, min_num=1,
                                          can_delete=False)
