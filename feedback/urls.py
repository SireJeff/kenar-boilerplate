
# app/feedback/urls.py
from django.urls import path
<<<<<<< HEAD
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

=======
from .views import suggestion_view, suggestion_thanks_view

urlpatterns = [
    path('suggestion/', suggestion_view, name='suggestion_form'),
    path('suggestion/thanks/', suggestion_thanks_view, name='suggestion_thanks'),
]
>>>>>>> 2d7a6a3a0897056e931dfa26b07f5525fa2bdb93
