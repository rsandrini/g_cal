from django.conf.urls.defaults import *
import os
from views import *

urlpatterns = patterns('',
    
    url(r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/listar_eventos/$', listar_eventos, name='listar_eventos'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/novo_evento/$', 'g_cal.views.novo_evento'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/(?P<evento_id>[a-zA-Z0-9.@_]+)/deletar_evento/$', 'g_cal.views.deletar_evento'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/(?P<evento_id>[a-zA-Z0-9.@_]+)/ver_evento/$', 'g_cal.views.ver_evento'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/(?P<evento_id>[a-zA-Z0-9.@_]+)/editar_evento/$', 'g_cal.views.editar_evento'),
    
    (r'^novo_calendario/$', 'g_cal.views.novo_calendario'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/deletar_calendario/$', 'g_cal.views.deletar_calendario'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/alterar_calendario/$', 'g_cal.views.alterar_calendario'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/ver_calendario/$', 'g_cal.views.ver_calendario'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/ver_calendario_g/$', 'g_cal.views.ver_calendario_g'),
    
    (r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/vincular_pessoa_calendario/$', 'g_cal.views.vincular_pessoa_calendario'),
    
    url(r'^listar_calendarios/$', listar_calendarios, name='listar_calendarios'),
    
    url(r'^$', listar_calendarios, name='listar_calendarios'),
    
    url(r'^(?P<calendario_id>[a-zA-Z0-9.@_]+)/listar_acl_calendario/$', listar_acl_calendario, name='listar_acl_calendario'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login',
                        {'template_name': 'g_cal/login.html'}),
                       
                           
    (r'^oauth2callback', 'plus.views.auth_return'),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')
}),
)
