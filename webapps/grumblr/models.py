from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.db.models import Max

# Create your models here.

class Tag(models.Model):
    content = models.CharField(max_length=420)


    def __unicode__(self):
        return self.content


class Post(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=42,blank=False)
    
    time = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)
    vote = models.IntegerField(default=0)

    tags = models.ManyToManyField(Tag,related_name='Tag+',default=[])

    def __unicode__(self):
        return self.post
      
    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(changetime="1970-01-01T00:00+00:00"):
        return Post.objects.filter(last_changed__gt=changetime).distinct()

    @staticmethod
    def get_changes_follower(request_user, changetime="1970-01-01T00:00+00:00"):
        profile=Profile.objects.get(user=request_user)
        followees = profile.followees.all()
        posts = Post.objects.filter(user__in=followees, last_changed__gt=changetime).distinct().order_by("time")
        return posts

    @staticmethod
    def get_changes_profile(profile_user, changetime="1970-01-01T00:00+00:00"):
        posts = Post.objects.filter(user=profile_user, last_changed__gt=changetime).distinct().order_by("time")
        return posts

    @staticmethod
    def get_max_time_follower(request_user):
        profile=Profile.objects.get(user=request_user)
        followees = profile.followees.all()
        posts = Post.objects.filter(user__in=followees).distinct()
        return posts.aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time_profile(profile_user):
        posts = Post.objects.filter(user=profile_user).distinct()
        return posts.aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"



class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    age = models.PositiveSmallIntegerField()
    bio = models.CharField(max_length=420, default="", blank=True)
    picture = models.ImageField(upload_to="profile_pictures", blank=True)
    followees = models.ManyToManyField(Post,related_name='Post+',)
    voting = models.ManyToManyField(Post, related_name='Posting+',)
    searching_following = models.ManyToManyField(Post, related_name='searching+', )
    searching_not_following = models.ManyToManyField(Post, related_name='searching_not+', )
    @staticmethod
    def get_profile(user):
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            print('The profile does not exist.')
        return profile

class Comment(models.Model):
    content = models.CharField(max_length=420)
    user = models.ForeignKey(User) 
    post = models.ForeignKey(Post)
    time = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    @staticmethod
    def get_changes(post_id, changeTime="1970-01-01T00:00+00:00"):
        post = Post.objects.get(id=post_id)
        diff_comments = Comment.objects.filter(post=post, last_changed__gt=changeTime).distinct().order_by("time")
        return diff_comments

    @staticmethod
    def get_max_time():
        return Comment.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time_follower(post_id):
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).distinct()
        return comments.aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

