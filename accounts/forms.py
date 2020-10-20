from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import AuthenticationForm

from .models import User
from .definitions import Gender


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Username'}))
        self.fields['password1'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'type': 'password',
                                                                                'class': 'form-control',
                                                                                'placeholder': 'Password'}))
        self.fields['password2'] = forms.CharField(required=True,
                                                   widget=forms.TextInput(attrs={'type': 'password',
                                                                                 'class': 'form-control',
                                                                                 'placeholder': 'Password Confirmation'}))
        GENDER_CHOICES = [(_.value[0], _.value[1]) for _ in Gender.__members__.values()]
        self.fields['gender'] = forms.ChoiceField(required=True,
                                                  choices=GENDER_CHOICES,
                                                  widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['phone'] = forms.CharField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Phone'}))
        self.fields['birthday'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Birthday: yyyy-mm-dd'}),
                                                  help_text='Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'gender', 'phone', 'birthday']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Username'}))
        self.fields['password'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'type': 'password',
                                                                                'class': 'form-control',
                                                                                'placeholder': 'Password'}))
