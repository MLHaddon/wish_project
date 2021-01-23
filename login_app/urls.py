from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.index),
  path('main', views.main),
  path('login', views.login),
  path('registration/add_user', views.add_user),
  path('success', views.success),
  path('logout', views.logout),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)