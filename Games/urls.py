from django.conf.urls import patterns, url

from Games import views

urlpatterns = patterns('',
    # ex: /game/
    url(r'^$', views.game_index, name='game_index'),
    # ex: /game/20141224/CHI_@_UTA # TODO /game/date/away-team_@_home-team
    url(r'^(?P<game_date>[0-9]{8})/(?P<away_team>\w{3,5})_@_(?P<home_team>\w{3,5})', views.game_page, name='game_page'),
)