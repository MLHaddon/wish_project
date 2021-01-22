from django.db import models
import re

class UserManager(models.Manager):
  def basic_validator(self, postData):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
    for user in User.objects.all():
      if postData['email'] == user.email:
        errors['email'] = 'Email already registered.'
    if not postData['first_name']:
      errors['first_name'] = 'Must Provide a First Name.'
    if not postData['last_name']:
      errors['last_name'] = 'Must Provide a Last Name.'
    if not postData['email']:
      errors['email'] = 'Must Provide an Email.'
    if not postData['password']:
      errors['password'] = 'Must Provide a Password'
    if not postData['pw_confirmation']:
      errors['pw_confirmation'] = 'Must Provide a Password Confirmation.'
    if len(postData['first_name']) < 2:
      errors['first_name'] = 'First Name must be at least Two characters in length.'
    if len(postData['last_name']) < 2:
      errors['last_name'] = 'Last Name must be at least Two characters in length.'
    if len(postData['password']) < 8:
      errors['password'] = 'Password must be at least 8 characters in length.'
    if not NAME_REGEX.match(postData['first_name']):
      errors['first_name'] = 'Invalid Character on First Name Property.'
    if not NAME_REGEX.match(postData['last_name']):
      errors['last_name'] = 'Invalid Character on "Last Name" Property.'
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = 'Invalid Email Format.'
    if postData['password'] != postData['pw_confirmation']:
      errors['password'] = 'Passwords Must Match.'
    return errors

class User(models.Model):
  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  email = models.TextField()
  password = models.TextField()
  objects = UserManager()
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
