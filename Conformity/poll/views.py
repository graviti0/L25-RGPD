from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views import View
from django.views.generic.edit import CreateView
from .forms import QuizForm
from django.shortcuts import render
from .models import Quiz, Question, Choice
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from .forms import QuizForm
from django.db import IntegrityError


@require_http_methods(["GET"])
def landing_page(request):
    return render(request, "landing_page.html")

@require_http_methods(["GET"])
def documentation(request):
    return render(request, "documentation.html")

@require_http_methods(["GET"])
def show_quiz(request):
    return render(request, "quiz.html")



questions = {
    1:{
        'text':"Combien de temps changez-vous vos mots de passe",
        'type':'RGPD',
        'reponse':{
            1:"Tous les 3 mois",
            2:"Tous les mois",
            3:"Plus de 3 mois"
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
    3:{
        'text':"Est-ce que votre organisme a une Délégué à la protection des données ?",
        'type':'BOTH',
        'reponse':{
            1:"Oui",
            2:"Non",
        },
    },
    
}
description_choice = {"RGPD" : "LALALALALAL",
                      "L25" : "LILILILILI",
                      "BOTH" : "LOLOLOLOLOLO"}


@require_http_methods(["GET"])
def show_questions(request):
    choice = request.GET.get('choice', 'BOTH')
    detail_choice = description_choice.get(choice)
    if not detail_choice:
        raise Http404('Erreur dans le choix')
    questions_choice = []
    for question in questions.values():
        if question["type"] == "BOTH" or question["type"] == choice or choice == "BOTH":
            questions_choice.append(question)
    context = {"questions":questions_choice}
    return render(request, "show_questions.html", {'context': context, 'detail_choice' : detail_choice, 'choice':choice})


@require_http_methods(["GET"])
def documentation_choice(request, choice):
    return render(request, "components/DocumentationChoice.html", {'choice': choice})



class CreateQuizView(CreateView):
    model = Quiz
    form = QuizForm
    success_url='quiz'

    def form_valid(self, form):
        self.object = form.save()
        choice = form.cleaned_data.get('choice')
        with transaction.atomic():
            quiz = self.object
            to_create = []
            question_number = 1
            for q in questions.values():
                if q["type"] == "Both" or q["type"] == choice or choice == "Both":
                    question_obj = Question(text=q["text"], quiz=quiz, number=question_number)
                    reponses = list(q["reponse"].values())
                    to_create.append((question_obj, reponses))
                    question_number += 1
            print(to_create)
            Question.objects.bulk_create([question_obj for question_obj, reponse in to_create])
            choice_bulk = []
            for question_obj, reponses in to_create:
                count = 0
                for text in reponses:
                    choice_bulk.append(Choice(
                        question=question_obj,
                        choice_text=text,
                        votes=count,
                    ))
                    count += 1
            Choice.objects.bulk_create(choice_bulk)
        return HttpResponseRedirect(reverse("quiz", args=[quiz.pk]))
    


class DetailQuizView(FormView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz.html'

    def get_queryset(self):
        return Quiz.objects.filter(pk=self.kwargs['pk'])
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)

    def get_success_url(self):
        return super().get_success_url()





