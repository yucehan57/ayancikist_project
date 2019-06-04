from django import forms
from userprofile.models import UserProfile

# when to use forms.Form and forms.ModelForm?
# forms.Form -> when DB is not to be directly impacted (Contact Form)
# forms.ModelForm -> when DB is directly impacted (User Registration )

class UserProfileForm(forms.ModelForm):
    # Form to extend & customize built-in
    # (django.contrib.auth.models.User) model
    class Meta:
        model = UserProfile
        exclude = ('user',)
