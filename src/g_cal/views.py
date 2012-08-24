# coding: utf-8
import os
import logging
import httplib2

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from oauth2client.django_orm import Storage
from oauth2client.client import OAuth2WebServerFlow
from g_cal.models import CredentialsModel
from g_cal.models import FlowModel
from apiclient.discovery import build

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import sys
from django.contrib.sites.models import Site
'''
@author: Rafael Sandrini Santos
@version: 0.2 2012-08-24
'''

'''
G_CAL 0.2
Integra com o calendário do google na versão 3 da api.
É Necessario ter e client_id e cliente_secret para autenticar.
Veja em https://code.google.com/apis/console/ seus dados 

Infos: Altere no /admin os dados de (site) para que ele tenha a referencia correta
na hora de executar a STEP2 da autenticação.

Funcionamento:
Após o cliente autorizar o acesso do APP na conta google ele registra a credencial no banco.
Este processo funciona apenas com as bibliotecas mais atuais do google calendar para python
Na versão "baixavel" deles na data de hoje ainda apresenta problemas, tive que atualizar manualmente
as bibliotecas do Python para conseguir rodar o projeto corretamente.

Os metodos, chamadas, atributos etc podem ser consultados em:
https://developers.google.com/google-apps/calendar/?hl=pt-BR

Versões deste app podem ser vistos em:
https://github.com/rafilsk/g_cal

Este código ainda é beta e precisa de muita refatoração, foi apenas para demonstrar e entender o 
funcionando da autenticação e troca de informações atraves do protocolos do google.

'''

_cliente_id     = ''
_cliente_secret = '' 
_user_agent     = '' #nome do APP registrado na google
_scope          = 'https://www.googleapis.com/auth/calendar'

flow = OAuth2WebServerFlow(
        client_id= _cliente_id,
        client_secret= _cliente_secret,
        scope= _scope,
        user_agent=_user_agent)

current_site = Site.objects.get_current()
STEP2_URI = "http://"+str(current_site)+"/g_cal/auth_return"

@login_required
def authentic(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        
        authorize_url = flow.step1_get_authorize_url(STEP2_URI)
        f = FlowModel(id=request.user, flow=flow)
        f.save()
        return authorize_url
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
            
        service = build(serviceName='calendar', version='v3', http=http) 
        
        return service


@login_required
def auth_return(request):
    f = FlowModel.objects.get(id=request.user)
    
    credential = f.flow.step2_exchange(request.REQUEST) #Zica aqui...
    
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    f.delete()
    return HttpResponseRedirect("/g_cal/")


@login_required
def listar_calendarios(request):
    try:
        service = authentic(request)
        calendar_list = service.calendarList().list().execute()
        return render_to_response('g_cal/lista_calendarios.html', {
            'agendas': calendar_list,
            })
    except:
        print "Redirecionando para autorização do usuario"
        return HttpResponseRedirect(service)
    
    
@login_required
def listar_eventos(request, calendario_id):
    service = authentic(request)
    events = service.events().list(calendarId=calendario_id).execute()
    return render_to_response('g_cal/listar_eventos.html', {
                'events': events, 'calendario_id': calendario_id,
                })



    
    
@login_required
def novo_evento(request, calendario_id):
    action = '/g_cal/'+calendario_id+'/novo_evento/'
    service = authentic(request)

    if request.POST:
        
        service = authentic(request)    
        
        # Manda para função que cria a estrutura de acordo com os filtros
        event = montar_evento(request)
        print event
        created_event = service.events().insert(calendarId=calendario_id, body=event).execute()
        return HttpResponseRedirect('/g_cal/'+calendario_id+'/listar_eventos') 
    
    
    else:
        return render_to_response('g_cal/form_evento.html',
                              {'action':action, 'calendario_id':calendario_id}, 
                              context_instance=RequestContext(request))
    
    
'''
Recebe a ID de uma calendario e o ID de um evento que será deletado
retorna para lista de eventos
'''    
@login_required
def deletar_evento(request, calendario_id, evento_id):
    
    service = authentic(request)
    service.events().delete(calendarId=calendario_id, eventId=evento_id).execute()

    return HttpResponseRedirect(reverse('g_cal:listar_eventos', args=[calendario_id])) 
    
@login_required
def ver_evento(request, calendario_id, evento_id):
    
    service = authentic(request)
    event = service.events().get(calendarId=calendario_id, eventId=evento_id).execute()

    return render_to_response('g_cal/ver_evento.html', {
            'event': event, 'calendario_id':calendario_id,
            })    
    
@login_required
def editar_evento(request, calendario_id, evento_id):
    action = '/g_cal/'+calendario_id+'/'+evento_id+'/editar_evento/'
    service = authentic(request)
    if request.POST:
    
        service = authentic(request)    
        event = montar_evento(request)
    
        updated_event = service.events().update(calendarId=calendario_id, eventId=evento_id, body=event).execute()
        
        return HttpResponseRedirect('/g_cal/'+calendario_id+'/listar_eventos') 
    else:
        event = service.events().get(calendarId=calendario_id, eventId=evento_id).execute()
        return render_to_response('g_cal/form_evento.html',
                              {'action':action, 'event':event, 'calendario_id':calendario_id}, 
                              context_instance=RequestContext(request))


@login_required
def novo_calendario(request):
    action = '/g_cal/novo_calendario/'
    service = authentic(request)

    if request.POST:
        
        service = authentic(request)    
        
        calendar = {
            'summary': request.POST.get("summary"),
            'timeZone': 'America/Sao_Paulo'
        }
    
        created_calendar = service.calendars().insert(body=calendar).execute()
        
        return HttpResponseRedirect(reverse('g_cal:listar_calendarios')) 

    else:
        return render_to_response('g_cal/form_calendario.html',
                              {'action':action}, 
                              context_instance=RequestContext(request))

    
@login_required
def deletar_calendario(request, calendario_id):
    
    service = authentic(request)     

    service.calendars().delete(calendario_id).execute()  

    return HttpResponseRedirect(reverse('g_cal:listar_calendarios'))     
  
    
@login_required
def alterar_calendario(request, calendario_id):
    
    service = authentic(request)     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId=calendario_id).execute()
    
    calendar['summary'] = 'Nome do calendario HFC'
    
    updated_calendar = service.calendars().update(calendarId=calendario_id, body=calendar).execute()

    
    return HttpResponseRedirect(reverse('g_cal:listar_calendarios'))     
    
        
@login_required
def ver_calendario(request, calendario_id):
    
    service = authentic(request)     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId=calendario_id).execute()
    
    return render_to_response('g_cal/ver_calendario.html', {
            'calendar': calendar,
            }) 

@login_required
def ver_calendario_g(request, calendario_id):
    
    service = authentic(request)     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId=calendario_id).execute()
    
    return render_to_response('g_cal/ver_calendario_g.html', {
            'calendar': calendar,
            }) 

@login_required
def nova_acl(request, calendario_id):
    
    action = '/g_cal/'+calendario_id+'/nova_acl/'
    service = authentic(request)

    if request.POST:
        
        service = authentic(request)    
        
        rule = {
            'role':request.POST.get("role"),
            'scope':
            {
                'type':request.POST.get("type"),
                'value':request.POST.get("value"),
            },
        }
    
        created_rule = service.acl().insert(calendarId=calendario_id, body=rule).execute()
        
        return HttpResponseRedirect(reverse('g_cal:listar_acl_calendario', args=[calendario_id])) 

    else:
        return render_to_response('g_cal/form_acl.html',
                              {'action':action}, 
                              context_instance=RequestContext(request))

@login_required
def deletar_acl(request, calendario_id, acl_id ):
    service = authentic(request)
    service.acl().delete(calendarId=calendario_id, ruleId=acl_id).execute()
    return HttpResponseRedirect(reverse('g_cal:listar_acl_calendario', args=[calendario_id])) 
    
    
@login_required
def listar_acl_calendario(request, calendario_id):
    service = authentic(request)
    acl = service.acl().list(calendarId=calendario_id).execute()
    
    
    return render_to_response('g_cal/listar_acl_calendario.html', {
        'acl': acl,'calendario_id':calendario_id,
    }) 
    
       
def montar_evento(request):
    _TimeZone = 'America/Sao_Paulo'
    prefixDateEvent = ""
    dateBeginEvent = ""
    dateEndEvent = ""
    
    rep_freq = ""
    event = ""
    dia_todo = request.POST.get("dia_todo")
    repetido = False
    
    if  dia_todo == None:
        dateBeginEvent = request.POST.get("dt_inicio")+'T'+request.POST.get("hr_inicio")+'.000-03:00'
        # O evento recebe a data de inicio para fim pois provavelmente irá terminar no mesmo dia...
        dateEndEvent = request.POST.get("dt_inicio")+'T'+request.POST.get("hr_fim")+'.000-03:00'

        prefixDateEvent = 'dateTime'
    else:
        dateEndEvent = dateBeginEvent = request.POST.get("dt_inicio")
        prefixDateEvent = 'date'
    
    if request.POST.get("cbo_repeticao") == "unico":
        repetido = False
        #Obrigatório uma data de Termino - Senão duplica para data de inicio
            
    else:
        repetido = True
        #intervalo de pulo dos eventos
        intervalo_n = request.POST.get("rep_a_cada")
        
        #Se houver repetição 
        if request.POST.get("cbo_repeticao") == "diario":
            rep_freq = "DAILY"
        elif request.POST.get("cbo_repeticao") == "semanal":
            rep_freq = "WEEKLY"
        elif request.POST.get("cbo_repeticao") == "mensal":
            rep_freq = "MONTHLY"
    
        
        #Quais dias da semana ?
        dias_semana = ""
        if request.POST.get("ds_dom"):
            dias_semana += "SU,"
        if request.POST.get("ds_seg"):
            dias_semana += "MO,"   
        if request.POST.get("ds_ter"):
            dias_semana += "TU,"
        if request.POST.get("ds_qua"):
            dias_semana += "WE,"
        if request.POST.get("ds_qui"):
            dias_semana += "TH,"
        if request.POST.get("ds_sex"):
            dias_semana += "FR,"
        if request.POST.get("ds_sab"):
            dias_semana += "SA,"                    
        # remove se houver o ultimo caracter (virgula)
        if dias_semana[-1::] == ",":
            dias_semana[-1::]
            dias_semana = dias_semana[:-1]

        #verifica se existe repetição em numero de ocorrencias
        if request.POST.get("tm_ocorrencias"):
            repeticao_vezes = request.POST.get("tm_ocorrencias")
            recurrence = "RRULE:FREQ="+rep_freq+";COUNT="+repeticao_vezes+";BYDAY="+dias_semana+";INTERVAL="+intervalo_n
  
        elif request.POST.get("tm_sempre"):
            # remove a data de termino
            recurrence = "RRULE:FREQ="+rep_freq+";BYDAY="+dias_semana+";INTERVAL="+intervalo_n
            
        elif request.POST.get("dt_fim"):
            #Determina o UNTIL - Trata a string de data
            dt_fim = request.POST.get("dt_fim").replace("-","")
            recurrence = "RRULE:FREQ="+rep_freq+";UNTIL="+dt_fim+"T000000Z;BYDAY="+dias_semana+";INTERVAL="+intervalo_n
      
    if repetido:
        event = {
         'summary': request.POST.get("titulo"),
         'description': request.POST.get("descricao"),

         'location': 'localizacao',
         'start': {
           prefixDateEvent : dateBeginEvent,
           'timeZone' : _TimeZone
         },
         'end': {
           prefixDateEvent : dateEndEvent,
           'timeZone' : _TimeZone
         },
           'recurrence': [recurrence],
         'attendees': [
           {
             'email': 'email@exemple.com.br',
             # Other attendee's data...
           },
           # ...
         ],
        }
    else:
        event = {
         'summary': request.POST.get("titulo"),
         'description': request.POST.get("descricao"),

         'location': 'localizacao',
         'start': {
           prefixDateEvent : dateBeginEvent,
           'timeZone' : _TimeZone
         },
         'end': {
           prefixDateEvent : dateEndEvent,
           'timeZone' : _TimeZone
         },
         'attendees': [
           {
             'email': 'email@exemple.com.br',
             # Other attendee's data...
           },
           # ...
         ],
        }
            
    return event    
    

  
    
    
    