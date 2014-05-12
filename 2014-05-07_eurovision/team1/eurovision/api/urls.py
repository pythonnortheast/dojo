from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import VoteView, CountryView, ScoreView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eurovision.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^vote/$', CountryView.as_view(), name='countries'),
    url(r'^vote/(?P<voting_country>\w+)/$', VoteView.as_view(), name='vote'),
    url(r'^scores/$', ScoreView.as_view(), name='scores'),
)
