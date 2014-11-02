from django.conf.urls import patterns, url

from Players import views

urlpatterns = patterns('',
    # ex: /player/ TODO Co ma się wyświetlać na tej stronie? Alfabetyczna lista wszystkich zawodników?
    # url(r'^$', views.index, name='index'),
    # ex: /player/Michael_Jordan/
    url(r'^(?P<player_fullname>\w+)/$', views.player_page, name='player_page'),
)