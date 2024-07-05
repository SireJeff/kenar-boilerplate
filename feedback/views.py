# app/feedback/views.py
from django.shortcuts import render, redirect
from .forms import SuggestionForm

def suggestion_view(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suggestion_thanks')  # Redirect to a thank you page
    else:
        form = SuggestionForm()
    return render(request, 'feedback/suggestion_form.html', {'form': form})

def suggestion_thanks_view(request):
    return render(request, 'feedback/suggestion_thanks.html')
