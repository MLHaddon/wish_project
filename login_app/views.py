from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
  if 'user_id' in request.session:
    return redirect('/wishes')
  return redirect('/main')

def main(request):
  return render(request, 'index.html')

def login(request):
  try:
    user = User.objects.get(email = request.POST['email'])
  except:
    messages.error(request, 'Email or Password Incorrect.')
    return redirect('/main')

  if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
    messages.error(request, 'Email or Password Incorrect.')
    return redirect('/main')
  request.session['user_id']  = user.id
  messages.success(request, 'Log In Successful.')
  return redirect('/wishes')

def success(request):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to view this page.')
    redirect('/main')
  context = {
    'user': User.objects.get(id = request.session['user_id'])
  }
  return render(request, 'success.html', context)
  
def logout(request):
  request.session.flush()
  return redirect('/main')

def add_user(request):
  # Set an error var
  errors = User.objects.basic_validator(request.POST)
  # Handle Errors
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/main')
  else:
    newPW = request.POST['password']
    pw_hash = bcrypt.hashpw(newPW.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    User.objects.create(
      first_name = request.POST['first_name'],
      last_name = request.POST['last_name'],
      email = request.POST['email'],
      password = pw_hash
    )
    user = User.objects.last()
    request.session['user_id']  = user.id
    messages.success(request, "User Account Successfully Created")
    return redirect('/wishes')
