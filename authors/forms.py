from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placehoder(field, placeholder_new_val):
    add_attr(field, 'placeholder', placeholder_new_val)

class RegisterForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placehoder(self.fields['username'], 'Your Username')
        add_placehoder(self.fields['email'], 'Your email')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your password'
            }
        ),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Passord must have at least one upppercase letter, '
            'one lowercase letter and one number'
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your password'
            }
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 
                  'last_name', 
                  'username',
                  'email',
                  'password',
        ]

        #exclude = ['first_name']
        labels = {
            'username': 'Username',
            'first_name': 'First name', 
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'The e-mail must be valid',
        }

        error_messages = {
            'username' : {
                'required': 'This field must not be empty',
                'max_length': 'This field must have less than 3 character',
                'invalid': 'This field is invalid'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'input text-input outra_classe',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
            })
        }
    
    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(valor)s no campo password',
                code = 'invalid',
                params={'valor': 'atenção'}
            )

        return data
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'Thiago' in data:
            raise ValidationError(
                'Não digite %(valor)s no campo first_name',
                code = 'invalid',
                params={'valor': 'Thiago'}
            )

        return data
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid',
            )

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                    'Another error'
                ],
            })