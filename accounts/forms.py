from django import forms
# from django.contrib.auth import password_validation
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm


class UserRegisterForm(UserCreationForm):
    """
    User creation form class.
    """
    username = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class':'form-control js-validate-username', 'name':'username', 'placeholder':"Username"}),
    )
    email = forms.EmailField(
        label='', 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email', 'name':'email', 'placeholder':"Email"}),
    )
    email2 = forms.EmailField(
        label='', 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email2', 'name':'confirm_email', 'placeholder':"Confirm Email"}),
    )
    password1 = forms.CharField(
        label='', 
        widget=forms.PasswordInput(attrs={'class':'form-control js-validate-password1', 'name':'password', 'placeholder':'Password'}),
        strip=False,
    )
    password2 = forms.CharField(
        label='', 
        widget=forms.PasswordInput(attrs={'class':'form-control js-validate-password2', 'name':'confirm_password', 'placeholder':'Confirm Password'}),
        strip=False,
    )

    class Meta:
        model   = User
        fields  = ['username', 'email', 'email2', 'password1', 'password2']   


    def clean_username(self):
        """
        Validate username.
        """
        username = self.cleaned_data.get("username")
        # check if the username has already been used.  
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("An account with this Username already exists.")
        return username 

    def clean_email2(self):
        """
        Validate email 2.
        """
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get('email2') 
        # check if the two emails match.
        if email1 != email2:
            raise forms.ValidationError('The two email fields didn’t match.')
        # check if the email has already been used.  
        if User.objects.filter(email__iexact=email2).exists():
            raise forms.ValidationError("An account with this Email already exists.")
        return email2


class EmailValidationOnForgotPassword(PasswordResetForm):
    """
    Override password reset form email field and its validation.
    """
    email = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control', 'name':'email', 'placeholder':"Email"})
    )

    def clean_email(self):
        """
        Validate email.
        """
        # fetch entered email
        email = self.cleaned_data['email']
        # check if the entered email doesn't exist
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Your email was entered incorrectly. Please enter it again.")
        return email


class PasswordFieldsOnForgotPassword(SetPasswordForm):
    """
    Override set password form password fields.
    """
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password1', 'id':'id_password1', 'placeholder':"New Password", 'required':True}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password2', 'id':'id_password2', 'placeholder':"Confirm Password", 'required':True}),
    )


class PasswordFieldsOnChangePassword(PasswordChangeForm):
    """
    Override password change form password fields.
    """
    old_password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control', 'placeholder':"Old Password", 'required':True}),
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password1', 'id':'id_password1', 'placeholder':"New Password", 'required':True}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password2', 'id':'id_password2', 'placeholder':"Confirm Password", 'required':True}),
    )
    