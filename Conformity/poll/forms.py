from django.forms import ModelForm
from .models import Quiz, Question, Choice
from django.forms.models import inlineformset_factory



class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = (
            'choice',
        )