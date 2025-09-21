from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-created_at')
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by('-created_at')
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from urllib.parse import urlencode


# Simple stubs to start OAuth flow with Google. These are intentionally
# minimal and do not store secrets in code. To enable, set the following
# environment variables / Django settings:
# - GOOGLE_CLIENT_ID
# - GOOGLE_CLIENT_SECRET
# - GOOGLE_REDIRECT_URI


def google_login(request):
	"""Redirect user to Google's OAuth2 consent screen (stub).

	If required settings are missing the view returns a 400 with instructions.
	"""
	client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
	redirect_uri = getattr(settings, 'GOOGLE_REDIRECT_URI', None)

	if not client_id or not redirect_uri:
		return JsonResponse({
			'error': 'google_not_configured',
			'detail': 'Configure GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI in settings.'
		}, status=400)

	params = {
		'client_id': client_id,
		'redirect_uri': redirect_uri,
		'response_type': 'code',
		'scope': 'openid email profile',
		'access_type': 'online',
		'prompt': 'select_account'
	}
	url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params)
	return HttpResponseRedirect(url)


def google_callback(request):
	"""Callback endpoint that Google will redirect to with ?code=..."""
	code = request.GET.get('code')
	if not code:
		return JsonResponse({'error': 'no_code', 'detail': 'Missing code in callback.'}, status=400)

	# In a real implementation you'd exchange the code for tokens here.
	return JsonResponse({'status': 'ok', 'message': 'Received code (stub).', 'code': code})


# Create your views here.
