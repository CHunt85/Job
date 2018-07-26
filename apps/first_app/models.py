from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) <= 0:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['first_name']) > 50:
            errors["first_name"] = "First name should be no more than 50 characters"
        if len(postData['last_name']) <= 0:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['last_name']) > 50:
            errors["last_name"] = "First name should be no more than 50 characters"
        if User.objects.filter(email = postData['email']).exists():
            errors['email'] = "Email already taken!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Not a valid email"
        elif len(postData['email']) <= 0:
            errors["email"] = "Email should be at least 8 characters"
        elif len(postData['email']) > 50:
            errors["email"] = "Email should be no more than 50 characters"
        if len(postData['password']) <= 0:
            errors["password"] = "Password should be at least 8 characters"
        if len(postData['password']) > 50:
            errors["password"] = "Password should be no more than 50 characters"
        if postData['con_pass'] != postData['password']:
            errors["con_pass"] = "Password should match"
        return errors
    def login_manager(self,postData):
        errors = {}
        if User.objects.filter(email=postData['email']).exists():
            user = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['passmatch']="Email and/or Password incorect."
        else:
            errors['passmatch']="Email and/or Password incorect."
        return errors

class Job_man(models.Manager):
    def job_manager(self,postData):
        errors = {}
        if len(postData['content1']) < 3:
            errors["content1"] = "Title should be at least 3 characters"
        if len(postData['content1']) > 50:
            errors["content1"] = "Title name should have no more than 50 characters"
        if len(postData['content2']) < 10:
            errors["content2"] = "Discription should be at least 10 characters"
        if len(postData['content2']) > 255:
            errors["content2"] = "Discription name should have no more than 255 characters"
        if len(postData['content3']) < 3:
            errors["content3"] = "Location should be at least 3 characters"
        if len(postData['content3']) > 255:
            errors["content3"] = "Location name should have no more than 255 characters"   
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length = 225)
    desc = models.CharField(max_length = 225)
    job = models.ForeignKey(User, related_name = "work")
    area= models.CharField(max_length = 225)
    loco= models.ManyToManyField(User, related_name = "there")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Job_man()