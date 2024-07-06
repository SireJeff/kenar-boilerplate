# app/feedback/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SuggestionForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
import requests
import urllib.parse

# API view to select a post
@api_view(['POST'])
def select_post(request):
    post_id = request.data.get('postId')
    try:
        post = Post.objects.get(id=post_id)
        # Logic for selecting the post (e.g., mark as selected)
        post.selected = True
        post.save()
        return Response({'success': True}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'success': False, 'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

# Redirect view to OAuth for authorization
def redirect_to_oauth(request):
    client_id = 'calico-solar-boa'
    redirect_uri = 'on-charming-labrador.ngrok-free.app/oauth/callback/'
    scope = 'USER_POSTS_GET'
    state = 'R1QDJBKOHX'  # Generate a random string for security

    query_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': urllib.parse.quote(redirect_uri, safe=''),
        'scope': scope,
        'state': state,
    }

    oauth_url = f"https://api.divar.ir/oauth2/auth?{urllib.parse.urlencode(query_params)}"
    return redirect(oauth_url)

# OAuth callback handling
def oauth_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    # Check if state matches the initial sent value

    if code:
        return exchange_code_for_token(code)
    else:
        return HttpResponse("Authorization failed")

# Exchange authorization code for access token
def exchange_code_for_token(code):
    token_url = "https://api.divar.ir/oauth2/token"
    client_id = 'calico-solar-boa'
    client_secret = '2b68c91a9beec2ace1d873cc5cdbac5f9b490b186555c16052990887e8466632193d0f22a541410f2384e7c095cca7acdba43fa2785d28ff302a9ddab42d4d1f'
    redirect_uri = 'on-charming-labrador.ngrok-free.app/oauth/callback/'

    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
    }

    response = requests.post(token_url, data=data)
    token_response = response.json()
    
    access_token = token_response.get('access_token')
    
    if access_token:
        request.session['access_token'] = access_token  # Store access token in session
        return use_access_token(access_token)
    else:
        return HttpResponse("Access token retrieval failed")

# Use access token to fetch user posts
def use_access_token(access_token):
    api_url = "https://api.divar.ir/v1/open-platform/finder/user-posts"
    headers = {
        'x-api-key': 'YOUR_API_KEY',  # Replace with your actual API key
        'x-access-token': access_token,
    }
    
    response = requests.get(api_url, headers=headers)
    posts = response.json().get('posts', [])
    
    return render(request, 'feedback/user_posts.html', {'posts': posts})

# View to retrieve user posts using stored access token
def get_user_posts(request):
    access_token = request.session.get('access_token')  # Assuming access_token is stored in session
    if not access_token:
        return HttpResponse("Access token not found in session")

    api_url = "https://api.divar.ir/v1/open-platform/finder/user-posts"
    headers = {
        "x-api-key": "eyJhbGciOiJSUzI1NiIsImtpZCI6InByaXZhdGVfa2V5XzIiLCJ0eXAiOiJKV1QifQ.eyJhcHBfc2x1ZyI6ImNhbGljby1zb2xhci1ib2EiLCJhdWQiOiJzZXJ2aWNlcHJvdmlkZXJzIiwiZXhwIjoxNzI1MTk2NDIyLCJqdGkiOiIxMWUxMjZmNy0zOTNlLTExZWYtOWZiYS1jYThjNTMxNGRjZTciLCJpYXQiOjE3MjAwMTI0MjIsImlzcyI6ImRpdmFyIiwic3ViIjoiYXBpa2V5In0.ZkEAoveAIBeWCnRpMUihTMw9TGvG-RKE37i-zwvVkShWTuM8x7jIUEeoQ5Txcu08iPgZTilNOBxz1v2_xYWmtQtFSntNPnv4b_wBfWbYfZCHM2CQeaXFRyewJRcTP_dMokxgYoFW8X6se6AgEAXFo3zEL2ynU7E1Cqx1spbHURGtvVxc2QrOQOwVy95leOlflAsqzVdG0SJvqKr6I6xstvuzNE_YRDkROpK7r3yv09muVWrXvec5vN2rw3nDTiX3BURVb7J0T4dWtj6Ol7m_ov07c7bu-A47zZQFTj6CaEOOTQKQVqo2eURDl0dpiJadDlaNdh-2K_97f37C-tXaYQ",
        "x-access-token": access_token,
    }

    response = requests.post(api_url, headers=headers)
    posts = response.json().get('posts', [])

    return render(request, 'feedback/user_posts.html', {'posts': posts})

# View for handling suggestion form submission
def suggestion_view(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suggestion_thanks')  # Redirect to a thank you page
    else:
        form = SuggestionForm()

    return render(request, 'suggestion_form.html', {'form': form})

# View for rendering the thank you page after suggestion submission
def suggestion_thanks_view(request):
    return render(request, 'suggestion_thanks.html')
