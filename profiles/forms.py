from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserForm(forms.ModelForm):
    """
    User model form.
    """
    username = forms.CharField(
        label='Username', 
        max_length=120,
        widget=forms.TextInput(attrs={'class':'form-control js-validate-username', 'name':'username'}),
    )
    first_name = forms.CharField(
        label='First Name',
        required=False, 
        max_length=120,
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'first_name'}),
    )
    last_name = forms.CharField(
        label='Last Name', 
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'last_name'}),
    )
    email = forms.EmailField(
        label='Email Address', 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email', 'name':'email'}),
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UserForm, self).__init__(*args, **kwargs)    

    def clean_username(self):
        """
        Validate username.
        """
        username = self.cleaned_data.get("username")
        # check if the username has already been used.  
        if User.objects.filter(username__iexact=username).exclude(username__iexact=self.request.user.username).exists():
            raise forms.ValidationError("An account with this Username already exists.")
        return username 

    def clean_email(self):
        """
        Validate email.
        """
        email = self.cleaned_data.get("email")
        # check if the email has already been used.  
        if User.objects.filter(email__iexact=email).exclude(email__iexact=self.request.user.email).exists():
            raise forms.ValidationError("An account with this Email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    """
    Profile model form.
    """
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput
    )
    bio = forms.CharField(
        label='Bio', 
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'bio'}),
    )
    facebook = forms.URLField(
        label='Facebook',
        required=False, 
        max_length=100,
        widget=forms.URLInput(attrs={'class':'form-control', 'name':'facebook'}),
    )
    twitter = forms.URLField(
        label='Twitter',
        required=False, 
        max_length=100,
        widget=forms.URLInput(attrs={'class':'form-control', 'name':'twitter'}),
    )
    instagram = forms.URLField(
        label='Instagram',
        required=False, 
        max_length=100,
        widget=forms.URLInput(attrs={'class':'form-control', 'name':'instagram'}),
    )
    website = forms.URLField(
        label='Website',
        required=False, 
        max_length=100,
        widget=forms.URLInput(attrs={'class':'form-control', 'name':'website'}),
    )
    private_account = forms.BooleanField(
        label='Private Account',
        required=False,
        initial=False,
    )

    class Meta:
        model  = UserProfile
        fields = ['photo', 'bio', 'facebook', 'twitter', 'instagram', 'website', 'private_account']