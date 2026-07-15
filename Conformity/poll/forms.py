from django.forms import ModelForm
from .models import Quiz, Question, Choice
from django.forms.models import inlineformset_factory


QuizForm = inlineformset_factory(Quiz, Question, fields=["text"], extra=3)