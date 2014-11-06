from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from BLM import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BLM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^player/', include('Players.urls')),
    url(r'^players/', include('Players.urls')),
    url(r'^team/', include('Teams.urls')),
    url(r'^teams/', include('Teams.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
