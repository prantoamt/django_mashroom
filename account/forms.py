from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "input100",
            "placeholder": "Username"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "input100",
            "placeholder": "Password"
        }
    ))


    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except:
            raise forms.ValidationError("Invalid Username")
        return username    

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            user = None        
        if user is not None and not user.check_password(password):
            raise forms.ValidationError("Invalid Password")
        elif user is None:
            pass
        else:
            return password    
