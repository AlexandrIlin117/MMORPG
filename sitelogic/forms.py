from django import forms
from .models import Publication
# from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class PublicationForm(forms.ModelForm):
   class Meta:
       model = Publication
       fields = [
           'publication_author',
           'publication_categories',
           'publication_header_announcement_news',
           'publication_content',
       ]