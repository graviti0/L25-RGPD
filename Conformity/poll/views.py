from django.http import HttpResponse, Http404
from django.views.generic.edit import FormView, CreateView, Lis
from .forms import QuizForm
from django.shortcuts import render
from .models import Quiz, Question
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ImproperlyConfigured



def landing_page(request):
    return render(request, "landing_page.html")


questions = {
    1:{
        'text':"Combien de temps changez-vous vos mots de passe",
        'type':'RGPD',
        'reponse':{
            1:"Tous les 3 mois",
            2:"Tous les mois",
            3:"Plusde 3 mois"
        },
    },
    2:{
        'text':"Est-ce que votre organisme a une charte sur l'évaluation des données ?",
        'type':'L25',
        'reponse':{
            1:"Oui",
            2:"Non",
            3:"Partiellement"
        },
    },
    
}
class CreateQuizView(CreateView):
    model = Quiz
    
    def form_valid(self, form):
        list_choice = ["RGPD", "L25", "Both"]
        choice = self.kwargs["choice"]
        if choice in list_choice:
            self.object = form.save()
            for question in questions:
                if question['type'] == choice:
                    
        raise Http404("Ce choix de réglement juridique n'existe pas")
    
        return super().form_valid(form)
    
    def get_success_url(self):
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy



#Voir pour decorator
@require_http_methods(["POST"])
def create_form(request, choice):
    if request.methods.POST:
        list_choice = ["RGPD", "L25", "Both"]
        if choice in list_choice:
            quiz = Quiz.objects.create()
            for question_id in questions:
                question = questions[question_id]
                if question['type'] == choice or choice == "Both":
                    Question.objects.create(quiz=quiz, text=question['text'], reponse_choice=question['reponse'])
        else:
            raise Http404("Ce choix de réglement juridique n'existe pas") 
        return HttpResponse(f'Vous avez créé un questionnaire {choice} numéro {Quiz.id}')
    raise Http404("Mauvaise méthode utilisée") 

class QuizFormView(FormView):
    template_name = "quiz.html"
    form_class = QuizForm
    success_url = reverse_lazy("/")



# Create your views here.
