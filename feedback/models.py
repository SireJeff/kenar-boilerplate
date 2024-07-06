# app/feedback/models.py
from django.db import models

class Suggestion(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# feedback/models.py
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class Tosts(models.Model):
    prompt =models.CharField(max_length=600)
    
    def __str__(self):
        return self.name