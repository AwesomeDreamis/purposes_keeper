from django import forms


class ResetPasswordForm(forms.Form):
    to_email = forms.EmailField(required=True)
