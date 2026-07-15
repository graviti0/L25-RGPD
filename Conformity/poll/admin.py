from django.contrib import admin
from .models import Quiz, Choice, Question
from django.contrib.admin.options import StackedInline, TabularInline
from django.template.loader import get_template
from django.db import models


class QuestionInline(StackedInline):
    model = Question
    extra = 2

class ChoiceInline(TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)

