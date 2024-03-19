from django.urls import path
from .views import index, signIn

urlpatterns = [
  path('', index),
  path('sign-in', signIn)
]