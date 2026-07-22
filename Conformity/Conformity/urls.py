"""
URL configuration for Conformity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from poll.views import landing_page, CreateQuizView, DetailQuizView, show_questions, documentation, show_quiz, documentation_choice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='accueil'),
    path('documentation/', documentation, name='documentation'),
    path('documentation/<str:choice>', documentation_choice, name='documentation_choice'),
    path('quiz/', show_quiz, name='quiz'),
    path('quiz/questions', show_questions, name='questions'),
    path('quiz/create/', CreateQuizView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/', DetailQuizView.as_view(), name='quiz-detail'),

]
