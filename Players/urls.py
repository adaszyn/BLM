from django.conf.urls import patterns, url

from Players import views

urlpatterns = patterns('',
    # ex: /player/
    url(r'^$', views.player_index, name='player_index'),
    # ex: /player/Michael_Jordan/
    url(r'^(?P<player_fullname>\w+)/$', views.player_page, name='player_page'),
)