from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'pages/home.html')

def signIn(request):
  return render(request, 'pages/sign-in.html')