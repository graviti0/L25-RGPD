from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_over = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.end_date:
            end_date = (self.start_date + timedelta(days=30)).date()
            self.end_date = end_date
        super().save(*args, **kwargs)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question')
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(default=1)
    text = models.CharField(max_length=255)

    def __str__(self):
        return 'Quiz n°' + str(self.quiz.id) + " Question n°" + str(self.number) + " : " + str(self.text)

    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choice')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    reponse = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.choice_text