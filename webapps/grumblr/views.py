# Create your views here.
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user

from django.contrib.auth import login, authenticate

from grumblr.forms import *

from django.http import HttpResponse, Http404
from mimetypes import guess_type

from django.db import transaction


import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

@login_required
def add_tag(request, post_id):
    context = {}
    form = TagForm(request.POST)
    context['form'] = form
    tag = form['tag'].value()

    post = Post.objects.get(id=post_id)
    new_tag = Tag.objects.create(content=tag)
    new_tag.save()
    post.tags.add(new_tag)
    post.save()

    posts = Post.objects.all().order_by("-time")
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    followees = profile.followees.all()
    voting = profile.voting.all()
    request_user_profile = Profile.objects.get(user=request.user)
    return render(request, 'grumblr/global_stream.html',
                  {'request_user_profile': request_user_profile, 'posts': posts, 'user': request.user,
                   'followees': followees, 'voting': voting})



@login_required
def add_tag_from_follow(request, post_id):
    context = {}
    form = TagForm(request.POST)
    context['form'] = form
    tag = form['tag'].value()

    post = Post.objects.get(id=post_id)
    new_tag = Tag.objects.create(content=tag)
    new_tag.save()
    post.tags.add(new_tag)
    post.save()

    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    request_user_profile = Profile.objects.get(user=request.user)
    posts = request_user_profile.followees.all().order_by('-time')
    request_user_followees = request_user_profile.followees.all()
    voting = request_user_profile.voting.all()
    return render(request, 'grumblr/follower_stream.html',
                  {'voting': voting, 'followees': request_user_followees, 'posts': posts, 'user': request.user,
                   'request_user_profile': request_user_profile})


@login_required
def add_tag_from_search(request, post_id):
    context = {}
    form = TagForm(request.POST)
    context['form'] = form
    tag = form['tag'].value()

    post = Post.objects.get(id=post_id)
    new_tag = Tag.objects.create(content=tag)
    new_tag.save()
    post.tags.add(new_tag)
    post.save()

    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    followees = profile.followees.all()
    voting = profile.voting.all()
    request_user_profile = Profile.objects.get(user=request.user)
    posts_following = profile.searching_following.all().order_by('-vote','-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote','-time')

    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': request_user_profile, 'posts_following': posts_following,
                   'posts_not_following': posts_not_following, 'user': request.user,
                   'followees': followees, 'voting': voting})


@login_required
def add_tag_from_profile(request, post_id):
    context = {}
    form = TagForm(request.POST)
    context['form'] = form
    tag = form['tag'].value()

    post = Post.objects.get(id=post_id)
    new_tag = Tag.objects.create(content=tag)
    new_tag.save()
    post.tags.add(new_tag)
    post.save()



    posts = Post.objects.filter(user=request.user).order_by("-time")


    followees = request.user.profile.followees.all()
    follow_number = 0
    for post in followees:
        follow_number = follow_number + 1

    voting = request.user.profile.voting.all()

    request_user_profile = Profile.objects.get(user=request.user)
    post_number = 0
    vote_number = 0
    for post in posts:
        post_number = post_number + 1
        vote_number = vote_number + post.vote

    return render(request, 'grumblr/profile.html',
                  {'profile': request_user_profile, 'follow_number': follow_number, 'post_number': post_number,
                   'vote_number': vote_number, 'request_user_profile': request_user_profile, 'posts': posts,
                   'user': request.user, 'followees': followees, 'voting': voting})


@login_required
def follow_from_search(request, post_id):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)

    profile.followees.add(post)
    profile.save()

    followees = profile.followees.all()
    voting = profile.voting.all()


    posts_following = profile.searching_following.all().order_by('-vote','-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote','-time')

    list_follow = list(posts_following)
    list_not_follow = list(posts_not_following)

    list_follow.append(post)
    list_not_follow.remove(post)

    profile.searching_following = list_follow
    profile.searching_not_following = list_not_follow

    profile.save()

    posts_following = profile.searching_following.all().order_by('-vote', '-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote', '-time')

    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': profile, 'posts_following': posts_following,
                   'posts_not_following': posts_not_following, 'user': request.user,
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


    posts_following = profile.searching_following.all().order_by('-vote','-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote','-time')

    list_follow = list(posts_following)
    list_not_follow = list(posts_not_following)
    try:
        list_follow.remove(post)
        list_not_follow.append(post)
    except ObjectDoesNotExist:
        raise Http404

    profile.searching_following = list_follow
    profile.searching_not_following = list_not_follow

    profile.save()

    posts_following = profile.searching_following.all().order_by('-vote', '-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote', '-time')

    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': profile, 'posts_following': posts_following,
                   'posts_not_following': posts_not_following, 'user': request.user,
                   'followees': followees, 'voting': voting})


@login_required
def follow_from_profile(request, post_id):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)

    profile.followees.add(post)
    profile.save()

    followees = profile.followees.all()


    posts_following = profile.searching_following.all().order_by('-vote','-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote','-time')

    list_follow = list(posts_following)
    list_not_follow = list(posts_not_following)
    if post in list_not_follow :
        list_follow.append(post)
        list_not_follow.remove(post)


    profile.searching_following = list_follow
    profile.searching_not_following = list_not_follow

    profile.save()

    posts = Post.objects.filter(user=request.user).order_by("-time")

    try:
        post_user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    followees = request.user.profile.followees.all()
    follow_number = 0
    for post in followees:
        follow_number = follow_number + 1

    voting = request.user.profile.voting.all()
    request_user_profile = Profile.objects.get(user=request.user)
    post_number = 0
    vote_number = 0
    for post in posts:
        post_number = post_number + 1
        vote_number = vote_number + post.vote

    return render(request, 'grumblr/profile.html',
                  {'profile': request_user_profile, 'follow_number': follow_number, 'post_number': post_number,
                   'vote_number': vote_number, 'request_user_profile': request_user_profile, 'posts': posts,
                   'user': request.user, 'followees': followees, 'voting': voting})



@login_required
def unfollow_from_profile(request, post_id):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)
    profile.followees.remove(post);
    profile.save()


    posts_following = profile.searching_following.all().order_by('-vote','-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote','-time')

    list_follow = list(posts_following)
    list_not_follow = list(posts_not_following)

    if post in list_follow :
        list_follow.remove(post)
        list_not_follow.append(post)


    profile.searching_following = list_follow
    profile.searching_not_following = list_not_follow

    profile.save()


    posts = Post.objects.filter(user=request.user).order_by("-time")

    followees = request.user.profile.followees.all()
    follow_number = 0
    for post in followees:
        follow_number = follow_number + 1

    voting = request.user.profile.voting.all()


    request_user_profile = Profile.objects.get(user=request.user)
    post_number = 0
    vote_number = 0
    for post in posts:
        post_number = post_number + 1
        vote_number = vote_number + post.vote

    return render(request, 'grumblr/profile.html',
                  {'profile': request_user_profile, 'follow_number': follow_number, 'post_number': post_number,
                   'vote_number': vote_number, 'request_user_profile': request_user_profile, 'posts': posts,
                   'user': request.user, 'followees': followees, 'voting': voting})





@login_required
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


    profile.searching_following = profile.searching_following.all().order_by('-vote')
    profile.searching_not_following = profile.searching_not_following.all().order_by('-vote')

    profile.save()

    posts_following = profile.searching_following.all().order_by('-vote','-time')
    posts_not_following = profile.searching_not_following.all().order_by('-vote','-time')
    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': profile, 'posts_following': posts_following,
                   'posts_not_following': posts_not_following, 'user': request.user,
                   'followees': followees, 'voting': voting})



@login_required
def vote_from_profile(request, post_id):
    post = Post.objects.get(id=post_id)
    if post in Profile.objects.get(user = request.user).voting.all() :
        profile = Profile.objects.get(user=request.user)
        voting = profile.voting.all()
        followees = profile.followees.all()

        posts_following = profile.searching_following.all().order_by('-vote','-time')
        posts_not_following = profile.searching_not_following.all().order_by('-vote','-time')
        return render(request, 'grumblr/search_result.html',
                      {'request_user_profile': profile, 'posts_following': posts_following,
                       'posts_not_following': posts_not_following, 'user': request.user,
                       'followees': followees, 'voting': voting})

    post.vote = post.vote + 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.add(post)
    profile.save()

    profile.searching_following = profile.searching_following.all().order_by('-vote')
    profile.searching_not_following = profile.searching_not_following.all().order_by('-vote')

    profile.save()

    posts = Post.objects.filter(user=request.user).order_by("-time")

    followees = request.user.profile.followees.all()
    follow_number = 0
    for post in followees:
        follow_number = follow_number + 1

    voting = request.user.profile.voting.all()

    request_user_profile = Profile.objects.get(user=request.user)
    post_number = 0
    vote_number = 0
    for post in posts:
        post_number = post_number + 1
        vote_number = vote_number + post.vote

    return render(request, 'grumblr/profile.html',
                  {'profile': request_user_profile, 'follow_number': follow_number, 'post_number': post_number,
                   'vote_number': vote_number, 'request_user_profile': request_user_profile, 'posts': posts,
                   'user': request.user, 'followees': followees, 'voting': voting})



@login_required
@transaction.atomic
def vote_from_follower(request, post_id):


    post = Post.objects.get(id=post_id)

    if post in Profile.objects.get(user = request.user).voting.all() :

        return redirect('/cooking/favorites')
    post.vote = post.vote + 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.add(post)
    profile.save()

    voting=profile.voting.all()
    followees = profile.followees.all()

    return redirect('/cooking/favorites')


@login_required
@transaction.atomic
def vote(request, post_id):

    post = Post.objects.get(id=post_id)



    post.vote = post.vote + 1
    post.save()

    profile = Profile.objects.get(user = request.user)
    profile.voting.add(post)
    profile.save()



    return redirect('/')


@login_required
@transaction.atomic
def search(request):
    context = {}
    form = SearchForm(request.POST)
    context['form'] = form
    key = form['key'].value()

    words = nltk.word_tokenize(key)
    tagged = nltk.pos_tag(words)
    key_list = []
    for word in tagged :
        print(word[1])
        if word[1] == 'NNS' or 'NN':
            key_list.append(word[0])

    error = 'Please try other key word'
    if not form.is_valid():
        return render(request, 'grumblr/search_result.html',
                      {'user': request.user,'error' : error})


    posts_following = Profile.objects.none()
    posts_not_following = Profile.objects.none()

    for eachkey in key_list:
        try:
            all_ids = request.user.profile.followees.values('id')
            posts_following1 = request.user.profile.followees.all().filter(tags__content__contains=eachkey).order_by(
                "-vote")
            posts_following2 = request.user.profile.followees.all().filter(content__contains=eachkey).order_by("-vote")

            posts_following = posts_following | posts_following1 | posts_following2

            posts_not_following1 = Post.objects.filter(content__contains=eachkey).exclude(id__in=all_ids).order_by("-vote")
            posts_not_following2 = Post.objects.filter(tags__content__contains=eachkey).exclude(id__in=all_ids).order_by(
                "-vote")
            posts_not_following = posts_not_following | posts_not_following1 | posts_not_following2

        except ObjectDoesNotExist:
            posts_following = []
            posts_not_following = []




    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404


    profile.searching_following = posts_following.order_by('-vote','-time')
    profile.searching_not_following = posts_not_following.order_by('-vote','-time')
    profile.save()
    followees = profile.followees.all()
    voting = profile.voting.all()
    request_user_profile = Profile.objects.get(user=request.user)
    return render(request, 'grumblr/search_result.html',
                  {'request_user_profile': request_user_profile, 'posts_following': posts_following, 'posts_not_following': posts_not_following, 'user': request.user,
                   'followees': followees,'voting' : voting})



def home(request):
    if not request.user.is_authenticated:
        posts = Post.objects.all().order_by("-time")
        return  render(request, 'grumblr/global_stream_anno.html', {'user' : request.user, 'posts' : posts,'voting':[],'followee':[]})

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

    return redirect('/')


@login_required
def profile(request, username):
    try:
        post_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

   
    posts = Post.objects.filter(user=post_user).order_by("-time")


    followees = request.user.profile.followees.all()
    follow_number = 0
    for post in followees:
        follow_number = follow_number + 1

    voting = request.user.profile.voting.all()

    request_user_profile = Profile.objects.get(user=request.user)
    post_number = 0
    vote_number = 0
    for post in posts :
        post_number = post_number + 1
        vote_number = vote_number + post.vote

    return render(request, 'grumblr/profile.html', {'profile':request_user_profile,'follow_number': follow_number,'post_number': post_number,'vote_number':vote_number,'request_user_profile':request_user_profile,'posts' : posts, 'user' : request.user, 'followees' : followees, 'voting' : voting})


@login_required
def follow_from_home(request, post_id):
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



    return redirect('/')

@login_required
def unfollow_from_follow(request, post_id):


    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)
    profile.followees.remove(post);
    profile.save()

    return redirect('/cooking/favorites')


@login_required
def unfollow_from_home(request, post_id):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    post = Post.objects.get(id=post_id)
    profile.followees.remove(post);
    profile.save()


    return redirect('/')

@login_required
def follower_stream(request):

    request_user_profile = Profile.objects.get(user=request.user)
    posts = request_user_profile.followees.all().order_by('-time')
    request_user_followees = request_user_profile.followees.all()
    voting = request_user_profile.voting.all()
    return render(request, 'grumblr/follower_stream.html', {'voting' : voting,'followees' : request_user_followees,'posts' : posts, 'user' : request.user, 'request_user_profile': request_user_profile})


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

    user = authenticate(username=user.username,
                            password=user.password)
    login(request, user)
    request_user_profile = Profile.objects.filter(user=request.user)
    

    return redirect('/cooking/profile/' + request.user.username)


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
    return redirect('/cooking/profile/' + request.user.username)

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

    return redirect('/cooking/main_page')



