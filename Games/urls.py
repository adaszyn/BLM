from django.conf.urls import patterns, url
from Games import views
urlpatterns = patterns('',
    # ex: /game/
    url(r'^$', views.game_index, name='game_index'),
)