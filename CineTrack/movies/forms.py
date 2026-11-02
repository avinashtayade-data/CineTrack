from django import forms
from .models import Movie
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MovieForm(forms.ModelForm):
    rating = forms.FloatField(
    min_value=0,
    max_value=10
    )


    class Meta:
        model = Movie
        fields = [
        'title',
        'genre',
        'release_year',
        'description',
        'rating'
    ]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']