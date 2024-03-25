from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, UserSignUpForm, ClientInfoForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST
from .custom.decorators import redirect_to_home_if_logged_in, client_profile_required
from django.conf import settings
from django.http import JsonResponse
import stripe

# Create your views here.
def index(request):
  return render(request, 'pages/home.html')

def signIn(request):
  if(request.method == 'POST'):
    form = LoginForm(request.POST)
    if form.is_valid():
      email=form.cleaned_data['email']
      password=form.cleaned_data['password']
      user = authenticate(request, username=email, password=password)
      if not user:
        form.add_error(None, 'Email or password is incorrect')
      else:
        login(request, user)
        return redirect('home')
  else:
    form = LoginForm()
  return render(request, 'pages/sign-in.html', {'form':form, 'submit_text':'Sign In'})

@redirect_to_home_if_logged_in
def signUp(request):
  if(request.method == 'POST'):
    form = UserSignUpForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      group_choice = form.cleaned_data['group']
      user.save()
      user.groups.add(group_choice)

      if(user.groups.filter(name='CLIENT').exists()):
        return redirect('sign-up-client')

      return redirect('sign-in')
    print(form.data['group'])
  else:
    form = UserSignUpForm()
  return render(request, 'pages/sign-up.html', {'form':form, 'submit_text':'Sign Up'})

@login_required(login_url='sign-in')
def signUpClient(request):
  
  if(request.method == 'POST'):
    form = ClientInfoForm(request.POST)
    if form.is_valid():
      clientInfo = form.save(commit=False)
      clientInfo.user = request.user
      clientInfo.save()
      return redirect('home')
  else:
    form = ClientInfoForm()

  return render(request, 'pages/sign-up-client.html', {'form':form, 'submit_text':'Sign Up'})

def logOut(request):
  logout(request)
  return redirect('home')

@permission_required('auth.can_view_admin_panel', login_url='sign-in')
def adminClients(request):
  return render(request, 'pages/admin-clients.html')

def membership(request):
  return render(request, 'pages/membership.html')


@require_POST
@client_profile_required
def createCheckOutSession(request):
  if request.method == 'POST':
    stripe.api_key = settings.STRIPE_SECRET_KEY
    DOMAIN = "http://127.0.0.1:8000/payment"
    try:
      price = stripe.Price.retrieve("price_1OyEIbI6yqRUcWu5ziTj7dvO")
      checkout_session = stripe.checkout.Session.create(
        line_items=[
          {
            'price': price.id,
            'quantity': 1,
          },
        ],
        mode='subscription',
        payment_method_types=['card'],
        customer_email=None,
        success_url= DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= DOMAIN + '/cancel',
      )
      return redirect(checkout_session.url)
    except Exception as e:
      print(e, e.__doc__)
  else:
    JsonResponse(status=404, data='Not Found')
  

def createPortalSession(request):
  if request.method == 'POST':
    stripe.api_key = settings.STRIPE_SECRET_KEY
    DOMAIN = "http://127.0.0.1:8000/payment"
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    checkout_session_id = request.form.get('session_id')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = DOMAIN

    portalSession = stripe.billing_portal.Session.create(
      customer=checkout_session.customer,
      return_url=return_url,
    )
    
    return redirect(portalSession.url)
  
def paymentSuccess(request):
  return render(request, 'pages/payment/payment_success.html')

def paymentCancel(request):
  return render(request, 'pages/payment/payment_cancel.html')
