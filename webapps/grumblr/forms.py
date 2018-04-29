from django import forms
from django.contrib.auth.models import User
from grumblr.models import *

class TagForm(forms.Form):


    tag = forms.CharField(max_length = 42)



    def clean(self):
        cleaned_data = super(TagForm, self).clean()

        tag = self.cleaned_data.get('tag')

        if not tag:
            raise forms.ValidationError("Tag cannot be empty.")

        return cleaned_data

class SearchForm(forms.Form):


    key = forms.CharField(max_length = 42)



    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        key = self.cleaned_data.get('key')

        if not key:
            raise forms.ValidationError("Search content cannot be empty.")

        return cleaned_data

class PostForm(forms.Form):
    post = forms.CharField(max_length = 500000,strip=False, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(PostForm, self).clean()

        post = self.cleaned_data.get('post')

        if not post:
            raise forms.ValidationError("Post cannot be empty.")

        return cleaned_data

class CommentForm(forms.Form):
    comment = forms.CharField(max_length = 420)

    def clean(self):
        
        cleaned_data = super(CommentForm, self).clean()

        comment = self.cleaned_data.get('comment')

        if not comment:
            raise forms.ValidationError("Comment cannot be empty.")
            
        return cleaned_data


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 40)
    last_name = forms.CharField(max_length = 40)
    username = forms.CharField(max_length = 40)
    password = forms.CharField(max_length = 100)
    confirm_password = forms.CharField(max_length = 100)
    email = forms.CharField(max_length = 100)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        

        # Check
        if User.objects.filter(username=username):
            raise forms.ValidationError("Username is already taken.")

        if not first_name:
            raise forms.ValidationError("First name is required.")
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        if not email:
            raise forms.ValidationError("Email is required.")
        if not password:
            raise forms.ValidationError("Password is required.")
        if not password2:
            raise forms.ValidationError("Password confirmation is required.")
        if password != password2:
            raise forms.ValidationError('Passwords did not match.')
        
        return cleaned_data


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    age = forms.IntegerField()
    bio = forms.CharField(max_length = 420)
    picture = forms.ImageField(required=False)


    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        age = self.cleaned_data.get('age')
        bio = self.cleaned_data.get('bio')

        
        if not first_name:
            raise forms.ValidationError("First name is required.")
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        if not type(age) is int:
            raise forms.ValidationError("Age must be an integer.")
        if not age >= 0:
            raise forms.ValidationError("Age must be a positive integer.")
        if not age <= 150:
            raise forms.ValidationError("Age is not valid")
        
        if not bio:
            raise forms.ValidationError("Bio length is invalid.")

        return cleaned_data

class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length = 100)
    confirm_password = forms.CharField(max_length = 100)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if not password:
            raise forms.ValidationError("Password is required.")
        if not password2:
            raise forms.ValidationError("Password is required.")
        if password != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

class EmailResetForm(forms.Form):
    email = forms.CharField(max_length = 100)

    def clean(self):
        cleaned_data = super(EmailResetForm, self).clean()

        email = self.cleaned_data.get('email')

        
        if not email:
            raise forms.ValidationError("Email is required.")
        if not User.objects.filter(email=email):
            raise forms.ValidationError("Email is not valid")

        return cleaned_data



