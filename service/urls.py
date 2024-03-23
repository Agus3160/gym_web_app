from django.urls import path
from .views import index, signIn, signUp, signUpClient, adminClients, logOut

urlpatterns = [

  #public routes
  path('', index, name='home'),
  path('sign-in', signIn, name='sign-in'),
  path('sign-up', signUp, name='sign-up'),
  path('logout', logOut, name='logout'),

  #client routes
  path('sign-up/client', signUpClient, name='sign-up-client'),

  #admin routes
  path('staff/clients', adminClients, name='staff-clients'),
]