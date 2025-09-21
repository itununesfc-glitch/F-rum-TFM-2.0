from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from urllib.parse import urlencode


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-created_at')
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by('-created_at')
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]


try:
	import requests
except Exception:
	requests = None

try:
	from jose import jwt
except Exception:
	jwt = None

try:
	from django.contrib.auth import get_user_model
	User = get_user_model()
except Exception:
	User = None


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
	# Exchange the code for tokens at Google's token endpoint
	token_url = 'https://oauth2.googleapis.com/token'
	client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
	client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
	redirect_uri = getattr(settings, 'GOOGLE_REDIRECT_URI', None)

	if not client_id or not client_secret or not redirect_uri:
		return JsonResponse({'error': 'google_not_configured', 'detail': 'Configure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET and GOOGLE_REDIRECT_URI in settings.'}, status=400)

	data = {
		'code': code,
		'client_id': client_id,
		'client_secret': client_secret,
		'redirect_uri': redirect_uri,
		'grant_type': 'authorization_code'
	}

	resp = requests.post(token_url, data=data, timeout=10)
	if resp.status_code != 200:
		return JsonResponse({'error': 'token_exchange_failed', 'detail': resp.text}, status=400)

	token_data = resp.json()
	id_token = token_data.get('id_token')
	access_token = token_data.get('access_token')

	if not id_token:
		return JsonResponse({'error': 'no_id_token', 'detail': 'Google did not return id_token.'}, status=400)

	# Decode/validate ID token (basic validation)
	try:
		# NOTE: In production you should verify signature and issuer/aud properly.
		decoded = jwt.get_unverified_claims(id_token)
	except Exception as e:
		return JsonResponse({'error': 'invalid_id_token', 'detail': str(e)}, status=400)

	email = decoded.get('email')
	email_verified = decoded.get('email_verified', False)
	name = decoded.get('name') or decoded.get('given_name')

	if not email:
		return JsonResponse({'error': 'no_email', 'detail': 'ID token does not contain email.'}, status=400)

	# Create or update user
	user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': name or ''})
	if not created:
		# Optionally update fields
		updated = False
		if user.email != email:
			user.email = email
			updated = True
		if name and user.first_name != name:
			user.first_name = name
			updated = True
		if updated:
			user.save()

	# Here you would create a session or return a token for the app
	return JsonResponse({'status': 'ok', 'message': 'User authenticated via Google (stub).', 'email': email, 'created': created})


# Create your views here.
