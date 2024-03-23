from django.shortcuts import render, redirect
from .forms import LoginForm, UserSignUpForm, ClientInfoForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import login, authenticate, logout
from .custom.decorators import redirect_to_home_if_logged_in

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
        form.add_error(None, 'Invalid credentials')
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
  form = ClientInfoForm()
  return render(request, 'pages/sign-up-client.html', {'form':form, 'submit_text':'Sign Up'})

def logOut(request):
  logout(request)
  return redirect('home')

@permission_required('auth.can_view_admin_panel', login_url='sign-in')
def adminClients(request):
  return render(request, 'pages/admin-clients.html')

