from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from users.models import CustomUser
from django.forms import ValidationError


class RegisterUserForm(UserCreationForm):
    """
    Form for registration of a new user.
    """
    phone_number = forms.CharField(min_length=12, max_length=12, label="Phone number with prefix",
                                   widget=forms.TextInput(attrs=dict(placeholder='+48700800900')))

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        """
        Validate phone number submitted by the user.
        :return: validated phone_number
        """
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('+48'):
            raise ValidationError("Phone number must start with +48 prefix")

        if not phone_number[3:].isdigit():
            raise ValidationError("Phone number after prefix must only contain digits")

        return phone_number
