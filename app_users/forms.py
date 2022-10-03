from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Textarea


class AuthForm(forms.Form):
    """Форма для логина"""

    username = forms.CharField(widget=Textarea(attrs={'placeholder': 'help'}))
    password = forms.CharField(widget=forms.PasswordInput)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form_control'


class RegisterForm(UserCreationForm):
    """Форма регистрации"""

    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    profile_img = forms.ImageField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class ProfileEditForm(forms.Form):
    """Форма для изменения профиля"""

    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    profile_img = forms.ImageField(required=False)
    profile_head_img = forms.ImageField(required=False)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=30, required=False, help_text='Username')

