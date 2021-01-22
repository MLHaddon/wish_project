from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('main', views.main),
  path('login', views.login),
  path('registration/add_user', views.add_user),
  path('success', views.success),
  path('logout', views.logout),
]