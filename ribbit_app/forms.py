from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags
from ribbit_app.models import Ribbit


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = User


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form


class RibbitForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'class': 'ribbitText'}))

    def is_valid(self):
        form = super(RibbitForm, self).is_valid()
        for f in self.errors.iterkeys():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error ribbitText'})
        return form

    class Meta:
        model = Ribbit
        exclude = ('user',)
