from django.conf.urls import patterns, url

from Teams import views

urlpatterns = patterns('',
    # ex: /team/ TODO /team/
    url(r'^$', views.team_index, name='team_index'),
    # ex: /team/team_name/
    url(r'^(?P<team_name>\w+)/$', views.team_page, name='team_page'),
)