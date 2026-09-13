from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required



def signup(request):
  t = {}
  t['title'] = "Sign Up"
  if request.method == "GET":
    t['form'] = CustomUserCreationForm()
    return render(request, "accounts/signup.html", {'template_data' : t})
  elif request.method == "POST":
    form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
    if form.is_valid():
      form.save()
      return redirect("accounts.login")
    else:
      t['form'] = form
      return render(request, 'accounts/signup.html',
                {'template_data': t})

@login_required
def logout(request):
  auth_logout(request)
  return redirect("home.index")

def login(request):
  t = {}
  t['title'] = "Login"
  if request.method == "GET":
    return render(request, "accounts/login.html", {'template_data' : t})
  elif request.method == "POST":
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
      t['error'] = 'Username/password not correct'
      return render(request, "accounts/login.html", {'template_data' : t})
    else:
      auth_login(request, user)
      return redirect("home.index")

@login_required
def orders(request):
  t = {}
  t['title'] = "Orders"
  t['orders'] = request.user.order_set.all()
  return render(request, 'accounts/orders.html', {'template_data': t})
