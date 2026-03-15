from django import forms
from .models import Post
# from .models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    # custom validation
    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:

            raise ValidationError(
                "Parollar mos emas!"
            )

        return cleaned_data


    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user

class LoginForm(forms.Form):
    username = forms.CharField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['bio', 'avatar']