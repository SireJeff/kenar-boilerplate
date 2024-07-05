# app/feedback/models.py
from django.db import models

class Suggestion(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
