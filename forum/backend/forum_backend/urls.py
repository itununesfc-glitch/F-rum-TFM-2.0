"""
URL configuration for forum_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from forum.views import PostViewSet, CommentViewSet, google_login, google_callback

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Google OAuth stubs
    path("api/auth/google/login/", google_login, name='google_login'),
    path("api/auth/google/callback/", google_callback, name='google_callback'),
]
