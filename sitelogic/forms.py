from django import forms
from .models import Publication
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PublicationForm(forms.ModelForm):
   class Meta:
       model = Publication
       fields = [
           'publication_author',
           'publication_categories',
           'publication_header_announcement_news',
           'publication_content',
       ]


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

class UserForm(forms.ModelForm):
   class Meta:
       model = User
       fields = [
           'email',
           'username',
           'first_name',
           'last_name',
       ]

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")
    # Verification_code = forms.CharField(label="Проверочный код")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )
