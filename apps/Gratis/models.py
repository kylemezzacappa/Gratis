from django.db import models
from datetime import datetime, date
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# Create your models here.
class UserManager(models.Manager):
    def regValidator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "email is not valid"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if (postData['password']) != postData["c_password"]:
            errors["c_password"] = "Password must match"
        users = User.objects.all()
        for user in users:
            if (postData['email']) == user.email:
                errors['email'] = "Email is already registered"
        return errors
  
    def log_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "email is invalid"
        if len(postData['password']) == 0:
            errors["password"] = "Password is required"
        if len(postData['email']) == 0:
            errors["email"] = "Email is required"
        user = User.objects.filter(email = postData['email'])
        if len(user):
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) != True:
                errors['password'] = 'Password is not correct'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BonusManager(models.Manager):
    def bonusValidator(self, postData):
        errors = {}
        if len(postData['my_bonus']) < 2:
            errors["my_bonus"] = "A bonus title should be at least 2 characters!"
        if len(postData['description']) < 10:
            errors["description"] = "Your description must be at least 10 characters!"
        return errors

    def bonusEditValidator(self, postData):
        errors = {}
        if len(postData['my_bonus']) < 2:
            errors["my_bonus"] = "A bonus titleshould be at least 5 characters!"
        if len(postData['description']) < 10:
            errors["description"] = "Your description must be at least 10 characters!"
        return errors

class Bonus(models.Model):
    my_bonus = models.CharField(max_length=200)
    description = models.CharField(max_length = 555)
    creator = models.ForeignKey(User, related_name="groupCreator")
    objects = BonusManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

