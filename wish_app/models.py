from django.db import models
from login_app.models import User

class WishManager(models.Manager):
  def basic_validator(self, postData):
    errors = {}
    if len(postData['item']) < 3:
      errors['item'] = 'Wish must be at least three characters in length.'
    if len(postData['desc']) < 3:
      errors['desc'] = 'Description must be at least three characters in length.'
    return errors


class Wish(models.Model):
  item = models.TextField()
  desc = models.TextField()
  user_that_posted = models.ForeignKey(User, related_name = 'wishes_of_user', on_delete = models.CASCADE)
  likes = models.IntegerField(default = 0)
  users_that_liked = models.ManyToManyField(User, related_name = 'wishes_liked')
  granted = models.BooleanField(default = False)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = WishManager()
