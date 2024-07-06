
# app/feedback/urls.py
from django.urls import path
from .views import suggestion_view, suggestion_thanks_view, select_post
# urls.py
from django.urls import path
from .views import redirect_to_oauth, oauth_callback

urlpatterns = [
    path('redirect/', redirect_to_oauth, name='redirect_to_oauth'),
    path('callback/', oauth_callback, name='oauth_callback'),
    path('suggestion/', suggestion_view, name='suggestion_form'),
    path('suggestion/thanks/', suggestion_thanks_view, name='suggestion_thanks'),
    path('api/select_post', select_post, name='select_post'),
]

