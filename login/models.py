from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from allauth.account.signals import user_signed_up, password_set, user_logged_in, user_logged_out 
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
import time, datetime
import os
import hashlib


# Create your models here.

# class User(models.Model):
#     userId = models.CharField(max_length=200)
#     userName = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     homeLocation = models.CharField(max_length=200)
#     #friends is an array of userIds
#     friends = ArrayField(models.CharField(max_length=200))
#     savedLocations = ArrayField(models.CharField(max_length=200), default=['Home,70.2333,-36.1239'])


#/***************************************************************************************
#*  REFERENCES
#*  Title: Real-time Chat Messenger (only for account and friends system)
#*  Author: CodingWithMitch
#*  Date: Oct 16th, 2020
#*  URL: https://www.youtube.com/playlist?list=PLgCYzUzKIBE9KUJZJUmnDFYQfVyXYjX6r
#*
#***************************************************************************************/


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return "codingwithmitch/default_profile_image.png"

def get_iamge_url():
    return "https://loremflickr.com/80/80?" + str(time.time())

class Account(AbstractBaseUser):
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30, unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    image_url               = models.CharField(max_length=1000, default="https://loremflickr.com/80/80?lock=" + str(int(hashlib.sha1(str(username).encode("utf-8")).hexdigest(), 16) % (10 ** 8)))
    profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email				= models.BooleanField(default=True)
    status                  = models.CharField(max_length=200, default=" ")
    savedLocations = ArrayField(models.CharField(max_length=200), default=['Home,70.233,-36.1239'])
    homeLongitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=7)
    homeLatitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=7)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

@receiver(post_save, sender=Account)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)

# class User(models.Model):
#     userId = models.CharField(max_length=200)
#     userName = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     homeLocation = models.CharField(max_length=200)
#     #friends is an array of userIds
#     # friends = ArrayField(models.CharField(max_length=200))
#     savedLocations = ArrayField(models.CharField(max_length=200), default=['Home,70.233,-36.1239'])
    




class FriendList(models.Model):

    user 				= models.OneToOneField(Account, on_delete=models.CASCADE, related_name="user")
    friends 			= models.ManyToManyField(Account, blank=True, related_name="friends") 


    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend.
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        """
        Remove a friend.
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone.
        """
        remover_friends_list = self # person terminating the friendship

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(remover_friends_list.user)

        content_type = ContentType.objects.get_for_model(self)

    @property
    def get_cname(self):
        """
        For determining what kind of object is associated with a Notification
        """
        return "FriendList"

    def is_mutual_friend(self, friend):
        """
        Is this a friend?
        """
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """
    A friend request consists of two main parts:
        1. SENDER
            - Person sending/initiating the friend request
        2. RECIVER
            - Person receiving the friend friend
    """

    sender 				= models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sender")
    receiver 			= models.ForeignKey(Account, on_delete=models.CASCADE, related_name="receiver")
    
    is_active			= models.BooleanField(blank=False, null=False, default=True)
    timestamp 			= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept a friend request.
        Update both SENDER and RECEIVER friend lists.
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                # sender_friend_list.save()
                self.is_active = False
                self.save()
            
    def decline(self):
        """
        Decline a friend request.
        Is it "declined" by setting the `is_active` field to False
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request.
        Is it "cancelled" by setting the `is_active` field to False.
        This is only different with respect to "declining" through the notification that is generated.
        """
        self.is_active = False
        self.save()

    @property
    def get_cname(self):
        """
        For determining what kind of object is associated with a Notification
        """
        return "FriendRequest"
        

class BaseLocation(models.Model):
    date_added = models.DateTimeField('date added') #def human redable name
    longitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=7)
    latitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=7)
    loc_name =  models.CharField(max_length=200)

class Place(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.PointField(null=True, blank=True)
    objects = models.Manager()
"""
class AuthWrapper(AbstractUser):
    savedPlaces = ArrayField(models.CharField(max_length=200))
    user_permissions = models.ForeignKey(User, related_name='wrapper_permissions', on_delete=models.CASCADE)


    def __str__(self):
        return self.email
"""


