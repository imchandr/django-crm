from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

    def __str__(self):
        return f"User - {self.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"User Profile-{self.user.username}"


class Leads(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent",on_delete=models.SET_NULL,null=True,blank=True)
    organisation = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    Category = models.ForeignKey("Category", on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"Leads - {self.first_name} {self.last_name}"
    

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Agent - {self.user.first_name}"

class Category(models.Model):
    ''' will have New, Contacted, Converted, Unconverted category'''
    name = models.CharField(max_length=25)
    organisation = models.ForeignKey("UserProfile",on_delete=models.CASCADE)


    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
    
