from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  path('', views.wishes),
  path('delete/<int:wish_id>', views.delete),
  path('edit/<int:wish_id>', views.edit_wish),
  path('edit/<int:wish_id>/edited', views.wish_edited),
  path('granted/<int:wish_id>', views.granted),
  path('like/<int:wish_id>', views.like_wish),
  path('new', views.new_wish),
  path('make_wish', views.make_wish),
  path('stats', views.stats),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)