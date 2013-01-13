from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from ribbit_app.models import Ribbit


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = User


class RibbitForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.widgets.Textarea())

    class Meta:
        model = Ribbit
        exclude = ('user',)
