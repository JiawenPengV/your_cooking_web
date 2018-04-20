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
    url(r'^global_stream$', grumblr.views.home, name='home'),
    url(r'^register$', grumblr.views.register, name='register'),
    
    url(r'^post', grumblr.views.post, name='post'),
    url(r'^profile/(?P<username>\w+)$', grumblr.views.profile, name='profile'),
    url(r'^photo/(?P<username>\w+)$', grumblr.views.get_profile_photo, name='photo'),
    url(r'^follow/(?P<post_id>\w+)$', grumblr.views.follow, name='follow'),
    
    url(r'^password_reset_form/(?P<username>\w+)$', grumblr.views.password_reset_form, name='reset_form'),
    url(r'^edit_profile$', grumblr.views.edit_profile, name='edit_profile'),
    url(r'^reset$', grumblr.views.reset_pass, name='reset_pass'),
    url(r'^reset_password$', grumblr.views.reset_password, name='reset_password'),
    url(r'^change_password$', grumblr.views.change_password, name='change_password'),
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'grumblr/login.html'}, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
  
    url(r'^follower_stream$', grumblr.views.follower_stream, name='follower_stream'),
    url(r'^unfollow/(?P<post_id>\w+)$', grumblr.views.unfollow, name='unfollow'),
    url(r'^unfollow_home/(?P<post_id>\w+)$', grumblr.views.unfollow_from_home, name='unfollow_from_home'),

    url(r'^delete/(?P<id>\d+)$', grumblr.views.delete, name='delete'),

    url(r'^password_reset_confirmation/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', grumblr.views.password_reset_confirmation, name='password_confirm'),
    
    #
    # url(r'^get-changes/(?P<time>.+)$', grumblr.views.get_changes),
    # url(r'^get-changes/?$', grumblr.views.get_changes),
    #
    # url(r'^add-comment/(?P<post_id>\d+)$', grumblr.views.add_comment),
    # url(r'^get-comments-changes/(?P<time>.+)/(?P<post_id>\d+)$', grumblr.views.get_comments_changes),
    # url(r'^get-changes-follower/(?P<time>.+)$', grumblr.views.get_changes_follower),
    # url(r'^get-changes-follower/?$', grumblr.views.get_changes_follower),
    # url(r'^get-comments-changes-for-post/(?P<time>.*)/(?P<post_id>\d+)$', grumblr.views.get_comments_changes_for_post),
    # url(r'^get-changes-profile/(?P<username>.+)/(?P<time>.+)$', grumblr.views.get_changes_profile),
    # url(r'^get-changes-profile/(?P<username>.+)/?$', grumblr.views.get_changes_profile),

    url(r'^search/?$', grumblr.views.search , name='search'),
    url(r'^get_search_changes/(?P<username>.+)/(?P<time>.+)$', grumblr.views.get_changes_profile),
    url(r'^get-changes-profile/(?P<username>.+)/?$', grumblr.views.get_changes_profile),

    url(r'^vote/(?P<post_id>.+)/?$', grumblr.views.vote, name='vote'),
    url(r'^devote/(?P<post_id>.+)/?$', grumblr.views.devote, name='devote'),

    url(r'^vote_from_follower/(?P<post_id>.+)/?$', grumblr.views.vote_from_follower, name='vote_from_follower'),
    url(r'^devote_from_follower/(?P<post_id>.+)/?$', grumblr.views.devote_from_follower, name='devote_from_follower'),

    url(r'^vote_from_search/(?P<post_id>.+)/?$', grumblr.views.vote_from_search, name='vote_from_search'),
    url(r'^devote_from_search/(?P<post_id>.+)/?$', grumblr.views.devote_from_search, name='devote_from_search'),

    url(r'^follow_from_search/(?P<post_id>.+)/?$', grumblr.views.follow_from_search, name='follow_from_search'),
    url(r'^unfollow_from_search/(?P<post_id>.+)/?$', grumblr.views.unfollow_from_search, name='unfollow_from_search'),


    url(r'^add_tag/(?P<post_id>.+)/?$', grumblr.views.add_tag, name='add_tag'),
]
