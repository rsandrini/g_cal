from django.conf.urls.defaults import *
import os
from views import *

urlpatterns = patterns('',
    # Example:
    url(r'^$', listar_eventos, name='listar_eventos'),
    
    (r'^novo_evento/$', 'g_cal.views.novo_evento'),
    
    (r'^del/$', 'g_cal.views.deletar_evento'),
    
    (r'^ver_evento/$', 'g_cal.views.ver_evento'),
    
    (r'^editar_evento/$', 'g_cal.views.editar_evento'),
    
    (r'^novo_calendario/$', 'g_cal.views.novo_calendario'),
    
    (r'^deletar_calendario/$', 'g_cal.views.deletar_calendario'),
    
    (r'^alterar_calendario/$', 'g_cal.views.alterar_calendario'),
    
    (r'^ver_calendario/$', 'g_cal.views.ver_calendario'),
    
    url(r'^listar_calendarios/$', listar_calendarios, name='listar_calendarios'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login',
                        {'template_name': 'g_cal/login.html'}),
                       
                           
    (r'^oauth2callback', 'plus.views.auth_return'),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')
}),
)
