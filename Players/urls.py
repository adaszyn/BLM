from django.conf.urls import patterns, url

from Players import views

urlpatterns = patterns('',
    # ex: /player/ TODO Co ma robić na tej stronie?
    # url(r'^$', views.index, name='index'),
    # ex: /player/firstname_lastname/ TODO Wielkość liter
    url(r'^(?P<player_fullname>\w+)/$', views.player_page, name='player_page'),
)