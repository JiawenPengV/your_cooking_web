# Create your views here.
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *
from grumblr.forms import *

from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core.mail import send_mail
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse


@login_required
def follow_from_search(request, post_id):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)

    profile.followees.add(post);
    profile.save()

    followees = profile.followees.all()
    voting = profile.voting.all()
    context = {'followees': followees, 'request_user_profile': profile}

    posts_following = profile.searching_following.all()
    posts_not_following = profile.searching_not_following.all()

    list_follow = list(posts_following)
    list_not_follow = list(posts_not_following)

    list_follow.append(post)
    list_not_follow.remove(post)

    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': profile, 'posts_following': list_follow,
                   'posts_not_following': list_not_follow, 'user': request.user,
                   'followees': followees, 'voting': voting})

@login_required
def unfollow_from_search(request, post_id):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)
    profile.followees.remove(post);
    profile.save()

    followees = profile.followees.all()
    voting = profile.voting.all()
    context = {'followees': followees, 'request_user_profile': profile}

    posts_following = profile.searching_following.all()
    posts_not_following = profile.searching_not_following.all()
    list_follow = list(posts_following)
    list_not_follow = list(posts_not_following)

    list_follow.remove(post)
    list_not_follow.append(post)

    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': profile, 'posts_following': list_follow,
                   'posts_not_following': list_not_follow, 'user': request.user,
                   'followees': followees, 'voting': voting})

@transaction.atomic
def vote_from_search(request, post_id):
    post = Post.objects.get(id=post_id)
    post.vote = post.vote + 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.add(post)
    profile.save()

    voting=profile.voting.all()
    followees = profile.followees.all()
    posts = profile.followees.all()
    context = {'voting': voting, 'followees' : followees}
    # return redirect('/grumblr/follower_stream')
    posts_following = profile.searching_following.all()
    posts_not_following = profile.searching_not_following.all()
    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': profile, 'posts_following': posts_following,
                   'posts_not_following': posts_not_following, 'user': request.user,
                   'followees': followees, 'voting': voting})

@transaction.atomic
def devote_from_search(request, post_id):
    post = Post.objects.get(id=post_id)
    post.vote = post.vote - 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.remove(post)
    profile.save()

    voting=profile.voting.all()
    followees = profile.followees.all()
    posts = profile.followees.all()
    context = {'voting': voting, 'followees': followees}
    # return redirect('/grumblr/follower_stream')
    posts_following = profile.searching_following.all()
    posts_not_following = profile.searching_not_following.all()
    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': profile, 'posts_following': posts_following,'posts_not_following': posts_not_following, 'user': request.user,
                   'followees': followees, 'voting': voting})



@transaction.atomic
def vote_from_follower(request, post_id):
    post = Post.objects.get(id=post_id)
    post.vote = post.vote + 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.add(post)
    profile.save()

    voting=profile.voting.all()
    followees = profile.followees.all()
    posts = profile.followees.all()
    context = {'voting': voting, 'followees' : followees}
    # return redirect('/grumblr/follower_stream')
    return render(request, 'grumblr/follower_stream.html',
                  {'request_user_profile': profile, 'posts': posts, 'user': request.user,
                   'followees': followees,'voting': voting})


@transaction.atomic
def devote_from_follower(request, post_id):
    post = Post.objects.get(id=post_id)
    post.vote = post.vote - 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.remove(post)
    profile.save()

    voting=profile.voting.all()
    followees = profile.followees.all()
    posts = profile.followees.all()
    context = {'voting': voting, 'followees': followees}
    # return redirect('/grumblr/follower_stream')
    return render(request, 'grumblr/follower_stream.html',
                  {'request_user_profile': profile, 'posts': posts, 'user': request.user,
                   'followees': followees, 'voting': voting})

@transaction.atomic
def vote(request, post_id):
    post = Post.objects.get(id=post_id)
    post.vote = post.vote + 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.add(post)
    profile.save()

    voting=profile.voting.all()
    followees = profile.followees.all()
    posts = Post.objects.all().order_by("-time")
    context = {'voting': voting, 'followees' : followees}

    return render(request, 'grumblr/global_stream.html',
                  {'request_user_profile': profile, 'posts': posts, 'user': request.user,
                   'followees': followees,'voting': voting})


@transaction.atomic
def devote(request, post_id):
    post = Post.objects.get(id=post_id)
    post.vote = post.vote - 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.remove(post)
    profile.save()

    voting=profile.voting.all()
    followees = profile.followees.all()
    context = {'voting': voting, 'followees': followees}
    return redirect('/')





@transaction.atomic
def search(request):
    context = {}
    form = SearchForm(request.POST)
    context['form'] = form
    key = form['key'].value()


    if not form.is_valid():
        return render(request, 'grumblr/global_stream.html', context)

    try:
        all_ids = request.user.profile.followees.values('id')
        posts_following = request.user.profile.followees.all().filter(content__contains=key).order_by("-vote")

        posts_not_following = Post.objects.filter(content__contains=key).exclude(id__in=all_ids).order_by("-vote")
        # tmp = []
        # # for each in posts_not_following.all() :
        # #     if each in posts_following.all() :
        # #         # print(each)
        # #         posts_not_following.delete(each.objects)
        # #
        # posts_following.union(posts_not_following)
        # posts = list(posts_following0 | posts_not_following
        # # posts = chain(posts_following , posts_not_following)
    except ObjectDoesNotExist:
        posts_following = []
        posts_not_following = []
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404


    profile.searching_following = posts_following
    profile.searching_not_following = posts_not_following
    profile.save()
    followees = profile.followees.all()
    voting = profile.voting.all()
    request_user_profile = Profile.objects.get(user=request.user)
    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': request_user_profile, 'posts_following': posts_following, 'posts_not_following': posts_not_following, 'user': request.user,
                   'followees': followees,'voting' : voting})


@transaction.atomic
def get_changes(request, time="1970-01-01T00:00+00:00"):
    try:

        max_time = Post.get_max_time()
        posts = Post.get_changes(time)
    except ObjectDoesNotExist:
        raise Http404

    context = {"max_time":max_time, "posts":posts,"username":request.user.username}
    return render(request, 'grumblr/posts.json', context, content_type='application/json')


@transaction.atomic
def get_comments_changes(request, post_id, time="1970-01-01T00:00+00:00"):
    if time == 'undefined':
        time="1970-01-01T00:00+00:00"
    try:
        max_time = Comment.get_max_time()

        comments = Comment.get_changes(post_id, time)

    except ObjectDoesNotExist:
        raise Http404

    context = {"max_time":max_time, "comments":comments}
    return render(request, 'grumblr/comments.json', context, content_type='application/json')


@login_required
@transaction.atomic
def add_comment(request, post_id):


    context = {}

    if request.method == 'GET':
        context['form'] = CommentForm()
        return render(request, 'grumblr/global_stream.html', context)

    form = CommentForm(request.POST)
    context['form'] = form


    if not form.is_valid():
        return render(request, 'grumblr/global_stream.html', context)

    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return HttpResponse("The post did not exist")

    new_comment = Comment(content=form.cleaned_data['comment'], user=request.user, post=post)
    new_comment.save()

    comments = Comment.objects.filter(post=post).order_by("-time")
    context['comments'] = comments

    return render(request, 'grumblr/comments.json', context, content_type='application/json')

# Returns all recent changes to the database, as JSON

@transaction.atomic
def get_changes_follower(request, time="1970-01-01T00:00+00:00"):
    try:
        max_time = Post.get_max_time_follower(request.user)
        posts = Post.get_changes_follower(request.user, time)

    except ObjectDoesNotExist:
        raise Http404

    context = {"max_time":max_time, "posts":posts, "username":request.user.username}
    return render(request, 'grumblr/posts.json', context, content_type='application/json')



@transaction.atomic
def get_comments_changes_for_post(request, post_id, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time="1970-01-01T00:00+00:00"
    try:
        max_time = Comment.get_max_time_follower(post_id)

        comments = Comment.get_changes(post_id, time)

    except ObjectDoesNotExist:
        raise Http404
    
    context = {"max_time":max_time, "comments":comments}
    return render(request, 'grumblr/comments.json', context, content_type='application/json')



@transaction.atomic
def get_changes_profile(request, username, time="1970-01-01T00:00+00:00"):
    try:
        profile_user = User.objects.get(username=username)
        max_time = Post.get_max_time_profile(profile_user)
        posts = Post.get_changes_profile(profile_user, time)
    
    except ObjectDoesNotExist:
        raise Http404


    
    context = {"max_time":max_time, "posts":posts,"username":request.user.username}
    return render(request, 'grumblr/posts.json', context, content_type='application/json')




def home(request):
    if not request.user.is_authenticated:
        posts = Post.objects.all().order_by("-time")
        return  render(request, 'grumblr/global_stream_anno.html', {'user' : request.user, 'posts' : posts})

    posts = Post.objects.all().order_by("-time")
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404


    followees = profile.followees.all()
    voting= profile.voting.all()
    request_user_profile = Profile.objects.get(user=request.user)
    return render(request, 'grumblr/global_stream.html', {'request_user_profile':request_user_profile,'posts' : posts, 'user' : request.user, 'followees' : followees, 'voting' : voting})


@login_required
def post(request):


    context = {}
    if request.method == 'GET':
        context['form'] = PostForm()
        return render(request, 'grumblr/global_stream.html', context)

    form = PostForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'grumblr/global_stream.html', context)

    new_post = Post(content=form.cleaned_data['post'], user=request.user)
    new_post.save()

    request_user_profile = Profile.objects.filter(user=request.user)
    
    posts = Post.objects.all().order_by("-time")
    context['request_user_profile']=request_user_profile
    context['posts'] = posts
    context['username'] = request.user.username
    return render(request, 'grumblr/posts.json', context, content_type='application/json')

@login_required
def delete(request, id):
    errors = []

    try:
        item_to_delete = Post.objects.get(id=id, user=request.user)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        raise Http404


    try:
        user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    request_user_profile = Profile.objects.filter(user=request.user)
    
    posts = Post.objects.filter(user=request.user).order_by('-time')
    context = {'posts' : posts, 'errors' : errors, 'profile' : user_profile,'request_user_profile':request_user_profile}
    return redirect('/')


@login_required
def profile(request, username):
    try:
        post_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

   
    posts_of_user = Post.objects.filter(user=post_user).order_by("-time")
   
    try:
        post_user_profile = Profile.objects.get(user=post_user)
    except ObjectDoesNotExist:
        raise Http404

    followees = request.user.profile.followees.all()

    request_user_profile = Profile.objects.get(user=request.user)
    context = {'posts' : posts_of_user, 'user' : post_user, 'profile' : post_user_profile, 'followees' : followees,'request_user_profile': request_user_profile}
    return render(request, 'grumblr/profile.html', context)

@login_required
def follow(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        raise Http404

    try:
        request_user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    request_user_profile.followees.add(post);
    request_user_profile.save()

    # request_user_followees=request_user_profile.followees.all()

    # # post_user_profile=Profile.objects.get(user=post_user)
    followees = request_user_profile.followees.all()
    # posts = Post.objects.filter(user__in=followees).order_by("-time")
    # request_user_profile = Profile.objects.filter(user=request.user)
    #
    context = { 'followees' : followees,'request_user_profile': request_user_profile}
    return redirect('/')

@login_required
def unfollow(request, post_id):


    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)
    profile.followees.remove(post);
    profile.save()

    
    followees = profile.followees.all()



    context = {'followees': followees, 'request_user_profile': profile}
    return redirect('/grumblr/follower_stream')


@login_required
def unfollow_from_home(request, post_id):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)
    profile.followees.remove(post);
    profile.save()

    followees = profile.followees.all()

    context = {'followees': followees, 'request_user_profile': profile}
    return redirect('/')

@login_required
def follower_stream(request):


    # posts = Post.objects.filter(user__in=followees).order_by("-time")
    request_user_profile = Profile.objects.get(user=request.user)
    posts = request_user_profile.followees.all()
    request_user_followees = request_user_profile.followees.all()
    return render(request, 'grumblr/follower_stream.html', {'followees' : request_user_followees,'posts' : posts, 'user' : request.user, 'request_user_profile': request_user_profile})


@login_required()
def change_password(request):
    errors = []
    context = {}
    try:
        profile = Profile.objects.get(user=request.user)
        request_user_profile = Profile.objects.filter(user=request.user)
    
    except ObjectDoesNotExist:
        raise Http404


    if request.method == 'GET':
        context['form'] = ChangePasswordForm()
        context['profile'] = profile
        context['request_user_profile'] =request_user_profile
        return render(request, 'grumblr/edit_profile.html', context)

    form = ChangePasswordForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        context['profile'] = profile
        context['request_user_profile'] =request_user_profile
        
        return render(request, 'grumblr/edit_profile.html', context)

    user = request.user
    user.set_password(form.cleaned_data['password'])
    user.save()


    posts = Post.objects.filter(user=request.user).order_by("-time")

    user = authenticate(username=user.username, \
                            password=user.password)
    login(request, user)
    request_user_profile = Profile.objects.filter(user=request.user)
    
    context = {'posts' : posts, 'errors' : errors, 'user' : request.user, 'profile' : profile,'request_user_profile':request_user_profile}
    return redirect('/grumblr/profile/' + request.user.username)


@login_required
def edit_profile(request):
    context = {}
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'GET':
        context['form'] = EditProfileForm()
        context['profile'] = profile
        return render(request, 'grumblr/edit_profile.html', context)
   

  
    form = EditProfileForm(request.POST, request.FILES)
    context['form'] = form

    if not form.is_valid():
        context['profile'] = profile
      
        return render(request, 'grumblr/edit_profile.html', context)

   
    posts_of_user = Post.objects.filter(user=request.user).order_by("-time")

    profile.age=form.cleaned_data['age']
    profile.bio=form.cleaned_data['bio']

    user = request.user
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    
    if form.cleaned_data['picture']:
        profile.picture=form.cleaned_data['picture']

    profile.save()
    request.user.save()
    
    request_user_profile = Profile.objects.filter(user=request.user)
    
    context = {'posts' : posts_of_user, 'user' : request.user, 'profile' : profile,'request_user_profile':request_user_profile}
    return redirect('/grumblr/profile/' + request.user.username)

# get the user profile photos

def get_profile_photo(request, username):
    
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404
    try:
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        raise Http404

    if not profile.picture:
        raise Http404
    content_type = guess_type(profile.picture.name)

    return HttpResponse(profile.picture, content_type=content_type)

@transaction.atomic
def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'grumblr/register.html', context)

    form = RegisterForm(request.POST)
    context['form'] = form

    
    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)


    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        password=form.cleaned_data['password'], \
                                        first_name=form.cleaned_data['first_name'], \
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],
                                        is_active=True)
    new_user.save()



    new_profile = Profile(age=0, user=new_user, bio='Introduction is here')
    new_profile.save()

    login(request, new_user)

    return redirect('/grumblr/global_stream')

@transaction.atomic
def reset_pass(request):
    return render(request, 'grumblr/password_reset.html')


@transaction.atomic
def reset_password(request):
    context = {}
    if request.method == 'GET':
        context['form'] = EmailResetForm()
        return render(request, 'grumblr/password_reset.html', context)

    form = EmailResetForm(request.POST)
    context['form'] = form

  
    if not form.is_valid():
        return render(request, 'grumblr/password_reset.html', context)
    try:
        user= User.objects.get(email=form.cleaned_data['email'])
    except ObjectDoesNotExist:
        raise Http404

    token = default_token_generator.make_token(user)

    email_body="""
    Please click the link below to verify your email address
    and complete the password resetting of your account:
    http://%s%s
    """ % (request.get_host(),
           reverse('password_confirm', args=(user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="jiawenp1@andrew.cmu.edu",
              recipient_list=[user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'grumblr/password_reset_confirmation.html', context)


@transaction.atomic
def password_reset_confirmation(request, username, token):
    context = {}
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    if not default_token_generator.check_token(user, token):

        return render(request, 'grumblr/error_page.html', context)

    context['user'] = user
    return render(request, 'grumblr/password_reset_form.html', context)

@transaction.atomic
def password_reset_form(request, username):
    context = {}
    if request.method == 'GET':
        context['form'] = ChangePasswordForm()
        return render(request, 'grumblr/password_reset_form.html', context)

    form = ChangePasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/password_reset_form.html', context)

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404
    user.set_password(form.cleaned_data['password'])
    user.save()

    return redirect('/grumblr/global_stream')


