from django import forms
from userprofile.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# when to use forms.Form and forms.ModelForm?
# forms.Form -> when DB is not to be directly impacted (Contact Form)
# forms.ModelForm -> when DB is directly impacted (User Registration )

### if I write in shell the following, I will get useful information
### about the model the Form is inheriting its fields from:
### > from accounts.forms import UserProfileForm
### > user1 = UserProfileForm()
### > user1
### <UserProfileForm bound=False, valid=Unknown, fields=(website, bio..)>
class UserProfileForm(forms.ModelForm):
    # Form to extend & customize built-in
    # (django.contrib.auth.models.User) model
    class Meta:
        model = UserProfile
        exclude = ('user',)


class ExtendedUserCreationForm(UserCreationForm):
    pass
    # email = forms.EmailField(required=True)
    # first_name = forms.CharField(max_length=30)
    # last_name = forms.CharField(max_length=30)
    #
    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'first_name',
    #               'last_name', 'password1', 'password2')
    #
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #
    #     user.email = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #
    #     if commit:
    #         user.save()
    #     return user
