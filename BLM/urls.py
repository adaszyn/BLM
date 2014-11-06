from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from BLM import settings
from Players import urls as PlayerUrls
from Teams import urls as TeamUrls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BLM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^players/(?P<player_fullname>\w+)/$', PlayerUrls.views.players_page),
    url(r'^teams/(?P<team_name>\w+)/$', TeamUrls.views.teams_page),
    url(r'^teams/', TeamUrls.views.teams_index),
    url(r'^player/', include('Players.urls')),
    url(r'^players/', PlayerUrls.views.players_index),
    url(r'^team/', include('Teams.urls')),
    url(r'^game/', include('Games.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
