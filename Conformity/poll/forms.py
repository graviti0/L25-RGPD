from django.forms import ModelForm
from .models import Quiz



class QuizForm(ModelForm):
    class meta:
        model = Quiz
        fields = ['questions.text', 'question.reponse', 'question.reponse_choice']

