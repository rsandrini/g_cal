import os
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'plus.views.index'),
    
    (r'^oauth2callback', 'plus.views.auth_return'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # adicioanr o URL do G_CAL
    (r'^g_cal/', include('g_cal.urls', namespace='g_cal')),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
                        {'template_name': 'plus/login.html'}),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
)