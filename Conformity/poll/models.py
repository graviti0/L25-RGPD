from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateField()
    is_over = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.end_date:
            end_date = (self.start_date + timedelta(days=30)).date()
            self.end_date = end_date
        super().save(*args, **kwargs)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question')
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)

    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text