from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateField()
    
    def save(self, *args, **kwargs):
        if not self.end_date:
            end_date = (self.start_date + timedelta(days=30)).date()
            self.end_date = end_date
        super().save(*args, **kwargs)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question')
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    reponse_choice = models.JSONField(default=dict)
    reponse = models.JSONField(default=dict, null=True)