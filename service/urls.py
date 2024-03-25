from django.urls import path
from .views import index, signIn, signUp, signUpClient, adminClients, logOut, membership, createPortalSession, paymentSuccess, paymentCancel, createCheckOutSession

urlpatterns = [

  #public routes
  path('', index, name='home'),
  path('sign-in', signIn, name='sign-in'),
  path('sign-up', signUp, name='sign-up'),
  path('logout', logOut, name='logout'),
  path('membership', membership, name='membership'),

  #client routes
  path('sign-up/client', signUpClient, name='sign-up-client'),

  #payment routes
  path('create-checkout-session', createCheckOutSession, name='create-checkout-session'),
  path('create-portal-session', createPortalSession, name='create-portal-session'),
  path('payment/success', paymentSuccess, name='payment-success'),
  path('payment/cancel', paymentCancel, name='payment-cancel'),

  #admin routes
  path('staff/clients', adminClients, name='staff-clients'),
]