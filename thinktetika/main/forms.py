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


ProfileForm = forms.inlineformset_factory(User, Profile, fields=('birth_date', 'avatar', 'phone_number',), can_delete=False,
                                          widgets={
                                              'birth_date': forms.DateInput(attrs={
                                                  'type': 'date',
                                                  'style': 'width:12%; align: center;',
                                              }),
                                          })
