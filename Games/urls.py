from django.conf.urls import patterns, url

from Games import views
urlpatterns = patterns('',
    # ex: /game/
    url(r'^$', views.game_index, name='game_index'),
    # ex: /game/2014-12-24/CHI_at_UTA
    url(r'^(?P<game_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<away_team_short>\w{3,5})_at_(?P<home_team_short>\w{3,5})/$',
        views.game_page, name='game_page'),
    # api
    # ex: /game/json/date=2014-12-24/
    url(r'^json/date=(?P<game_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.get_games_by_date, name='game_index'),
    # ex: /game/json/date=2014-12-24&limitTo=2/
    url(r'^json/date=(?P<game_date>[0-9]{4}-[0-9]{2}-[0-9]{2})&limitTo=(?P<quantity>\d)&dir=(?P<direction>[0-1]{1})/$', views.get_gamesdates, name='game_index')
)

