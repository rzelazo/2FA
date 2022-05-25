from django import forms
from .models import Code


class CodeForm(forms.ModelForm):
    """
    Form for submitting SMS verification code input from the user.
    """
    number = forms.CharField(label='Code',
                             widget=forms.TextInput(attrs=dict(placeholder='Enter SMS verification code...')))

    class Meta:
        model = Code
        fields = ['number']
