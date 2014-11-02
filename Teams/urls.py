from django.conf.urls import patterns, url

from Teams import views

urlpatterns = patterns('',
    # ex: /team/ TODO Wyświetlanie spisu drużyn
    # url(r'^$', views.index, name='index'),
    # ex: /team/team_name/ TODO Wielkość liter
    url(r'^(?P<team_name>\w+)/$', views.team_page, name='team_page'),
)