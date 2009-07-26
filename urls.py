from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#from twitterauth.views import twitter_signin, twitter_return
#from feed.views import twitter_feed

from feed.views import friendfeed_feed

from views import welcome

urlpatterns = patterns('',
    # Example:
    # (r'^doubleblind/', include('doubleblind.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),

    url(r'^$', welcome, name='welcome'),
#    url('^login/$', twitter_signin, name='login'),  
#    url('^return/$', twitter_return, name='return'),  
#    url('^feed/([^/]+)$', twitter_feed, name='feed'),  
    url('^feed/$', friendfeed_feed, name='feed'),  
)
