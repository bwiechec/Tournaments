from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import DateInput

from .models import UserUser


class CustomUserCreationForm(UserCreationForm):
    birth_date = DateInput()

    class Meta:
        model = UserUser
        #fields = ('email', 'birth_date')
        fields = ['username', 'email', 'birth_date']
        widgets = {'birth_date': DateInput(
                    format=('%Y-%m-%d'),
                    attrs={'class': 'form-control',
                           'placeholder': 'Select a date',
                           'type': 'date'
              })
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserUser
        fields = ('email', )


class CustomUserAuthenticationForm(AuthenticationForm):

    class Meta:
        model = UserUser
        fields = ('email', )