"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url

import django.contrib.auth.views


import grumblr.views

urlpatterns = [
    url(r'^$', grumblr.views.home),
    url(r'^main_page$', grumblr.views.home, name='home'),
    url(r'^register$', grumblr.views.register, name='register'),
    
    url(r'^post', grumblr.views.post, name='post'),
    url(r'^profile/(?P<username>\w+)$', grumblr.views.profile, name='profile'),
    url(r'^photo/(?P<username>\w+)$', grumblr.views.get_profile_photo, name='photo'),
    url(r'^follow/(?P<post_id>\w+)$', grumblr.views.follow_from_home, name='follow_from_home'),
    


    url(r'^edit_profile$', grumblr.views.edit_profile, name='edit_profile'),

    url(r'^change_password$', grumblr.views.change_password, name='change_password'),
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'grumblr/login.html'}, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
  
    url(r'^favorites$', grumblr.views.follower_stream, name='follower_stream'),
    url(r'^unfollow/(?P<post_id>\w+)$', grumblr.views.unfollow_from_follow, name='unfollow_from_follow'),
    url(r'^unfollow_home/(?P<post_id>\w+)$', grumblr.views.unfollow_from_home, name='unfollow_from_home'),


    url(r'^search/?$', grumblr.views.search , name='search'),

    url(r'^vote/(?P<post_id>.+)/?$', grumblr.views.vote, name='vote'),

    url(r'^vote_from_follower/(?P<post_id>.+)/?$', grumblr.views.vote_from_follower, name='vote_from_follower'),

    url(r'^vote_from_search/(?P<post_id>.+)/?$', grumblr.views.vote_from_search, name='vote_from_search'),

    url(r'^follow_from_search/(?P<post_id>.+)/?$', grumblr.views.follow_from_search, name='follow_from_search'),
    url(r'^unfollow_from_search/(?P<post_id>.+)/?$', grumblr.views.unfollow_from_search, name='unfollow_from_search'),


    url(r'^add_tag/(?P<post_id>.+)/?$', grumblr.views.add_tag, name='add_tag'),
    url(r'^add_tag_from_follow/(?P<post_id>.+)/?$', grumblr.views.add_tag_from_follow, name='add_tag_from_follow'),

    url(r'^add_tag_from_search/(?P<post_id>.+)/?$', grumblr.views.add_tag_from_search, name='add_tag_from_search'),
    url(r'^add_tag_from_profile/(?P<post_id>.+)/?$', grumblr.views.add_tag_from_profile, name='add_tag_from_profile'),

    url(r'^follow_from_profile/(?P<post_id>.+)/?$', grumblr.views.follow_from_profile, name='follow_from_profile'),
    url(r'^unfollow_from_profile/(?P<post_id>.+)/?$', grumblr.views.unfollow_from_profile, name='unfollow_from_profile'),

    url(r'^vote_from_profile/(?P<post_id>.+)/?$', grumblr.views.vote_from_profile, name='vote_from_profile'),

]
