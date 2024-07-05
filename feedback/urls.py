
# app/feedback/urls.py
from django.urls import path
from .views import suggestion_view, suggestion_thanks_view

urlpatterns = [
    path('suggestion/', suggestion_view, name='suggestion_form'),
    path('suggestion/thanks/', suggestion_thanks_view, name='suggestion_thanks'),
]
