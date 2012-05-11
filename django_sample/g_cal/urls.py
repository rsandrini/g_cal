from django.conf.urls.defaults import *
import os


urlpatterns = patterns('',
    # Example:
    (r'^$', 'django_sample.g_cal.views.listar_eventos'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login',
                        {'template_name': 'g_cal/login.html'}),
                       
                           
    (r'^oauth2callback', 'django_sample.plus.views.auth_return'),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')
}),
)
