from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from .models import User
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext, ugettext_lazy as _

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class' :'form-control',
                'placeholder' : 'Email',
                'required' : 'True',
            }
        )
    )
    birth = forms.DateField(label="birth", required=True, widget=forms.DateInput(
        attrs={
                'class' :'form-control',
                'placeholder' : 'birth ex) 1995-01-02',
                'required' : 'True',
            }
    ))
    username = forms.RegexField(label="ID", max_length=30,
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
        attrs={
                'class' :'form-control',
                'placeholder' : 'ID',
                'required' : 'True',
        }),
        error_messages={
            'invalid': "this value may contain only letters, numbers and @/./+/-/_ characters.",
        }
    )
    phone = forms.CharField(label="phone", max_length=50,
        widget=forms.TextInput(
        attrs={
                'class' :'form-control',
                'placeholder' : 'phone',
                'required' : 'True',
        }    
    ))
    first_name = forms.CharField(label="name", max_length=30,
        widget=forms.TextInput(
        attrs={
                'class' :'form-control',
                'placeholder' : 'name',
                'required' : 'True',
        }
    ))    
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'class' :'form-control',
                'placeholder' : 'Password',
                'required' : 'True',
            }
        ))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                'class' :'form-control',
                'placeholder' : 'Password confirm',
                'required' : 'True',
            }
        ),
        help_text=_("Enter the same password as above, for verification."))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username","first_name","email","phone","birth",]
        #fields = '__all__'
    

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ["first_name","email","phone","birth",]

class UserPassChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("기존 비밀번호"),
    widget=forms.PasswordInput(
        attrs={
            'class' :'form-control',
            'placeholder' : 'Password',
            'required' : 'True',
        }
    ))
    new_password1 = forms.CharField(label=_("새로운 비밀번호"),
        widget=forms.PasswordInput(
            attrs={
                'class' :'form-control',
                'placeholder' : 'Password confirm',
                'required' : 'True',
            }
        ))
    new_password2 = forms.CharField(label=_("비밀번호 확인"),
    widget=forms.PasswordInput(
        attrs={
            'class' :'form-control',
            'placeholder' : 'new Password',
            'required' : 'True',
        }
    ),
    help_text=_("Enter the same password as above, for verification."))
    class Meta:
        model = get_user_model()
        fields =  ['old_password','new_password1','new_password2',]