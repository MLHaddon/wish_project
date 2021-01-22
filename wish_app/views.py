from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from login_app.models import User
from .models import Wish

def wishes(request):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  context = {
    'user': User.objects.get(id = request.session['user_id']),
    'wishes': Wish.objects.filter(user_that_posted = User.objects.get(id = request.session['user_id'])),
    'granted_wishes': Wish.objects.filter(granted = True)
  }
  return render(request, 'wishes.html', context)

def stats(request):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  # Set the vars
  user = User.objects.get(id = request.session['user_id'])
  pending_wishes = Wish.objects.filter(granted = False)
  granted_wishes = Wish.objects.filter(granted = True)

  # Set the counts
  total_granted = 0
  my_granted = 0
  my_pending = 0

  for wish in granted_wishes:
    total_granted += 1
    if wish.user_that_posted == user:
      my_granted += 1
  for wish in pending_wishes:
    if wish.user_that_posted == user:
      my_pending += 1

  context = {
    'total': total_granted,
    'my_granted': my_granted,
    'my_pending': my_pending
  }
  return render(request, 'stats.html', context)

def delete(request, wish_id):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  wish = Wish.objects.get(id = wish_id)
  wish.delete()
  return redirect('/wishes')

def edit_wish(request, wish_id):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  context = {
    'user': User.objects.get(id = request.session['user_id']),
    'wish': Wish.objects.get(id = wish_id)
  }
  return render(request, 'edit_wish.html', context)

def wish_edited(request, wish_id):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  errors = Wish.objects.basic_validator(request.POST)
  if errors:
    for key, val in errors.items():
      messages.error(request, val)
      return redirect(f'/wishes/edit/{wish_id}')
  wish = Wish.objects.get(id = wish_id)
  wish.item = request.POST['item']
  wish.desc = request.POST['desc']
  wish.save()
  return redirect('/wishes')

def granted(request, wish_id):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  wish = Wish.objects.get(id = wish_id)
  wish.granted = True
  wish.save()
  return redirect('/wishes')


def new_wish(request):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  context = {
    'user': User.objects.get(id = request.session['user_id'])
  }
  return render(request, 'make_wish.html', context)

def make_wish(request):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  errors = Wish.objects.basic_validator(request.POST)
  item = request.POST['item']
  desc = request.POST['desc']
  if not item:
    errors['item'] = 'Item Field is required.'
  if not desc:
    errors['desc'] = 'Description field is required.'
  if errors:
    for key, val in errors.items():
      messages.error(request, val)
      return redirect('/wishes/new')
  Wish.objects.create(
    item = item,
    desc = desc,
    user_that_posted = User.objects.get(id = request.session['user_id'])
  )
  wish = Wish.objects.last()
  wish.users_that_liked.add(User.objects.get(id = request.session['user_id']))
  wish.save()
  return redirect('/wishes')

def like_wish(request, wish_id):
  if not 'user_id' in request.session:
    messages.error(request, 'You must be logged in to do that.')
    return redirect('/')
  wish = Wish.objects.get(id = wish_id)
  wish.users_that_liked.add(User.objects.get(id = request.session['user_id']))
  wish.save()
  return redirect('/wishes')