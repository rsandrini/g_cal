# coding: utf-8
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
import httplib2

'''
@author: Rafael Sandrini Santos
@version: 0.1 2012-08-14

Metodo de listar eventos do calendario principal GOOGLE API CALENDAR 3.0
Altere os dados de cliente_id, cliente_secret e developer_key
No primeiro acesso sera aberto uma nova aba/janela para autorizacao 
de acesso ao google Calendar. isto e conhecido como "consentimento do usuario"
Basta selecionar que autoriza... O token e trocado automaticamente e ele deve
mostrar uma lista com as tarefas da agenda principal.
'''

"""
Limpar estes dados antes de enviar ao GIT
"""
_cliente_id = "762839273641-ccoho801k4gtgl77sipud30s8rvm3sn1.apps.googleusercontent.com"
_cliente_secret = "DYBBc2Rs8_y7u5_Aj4loihuu"
_developer_key = "AIzaSyDUh0YTPqD0FBy7B0lUoi9YCbeB0WtqvlY"

def authentic():
    FLOW = OAuth2WebServerFlow(
    client_id=_cliente_id,
    client_secret=_cliente_secret,
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Calendar/1.0')
    
    storage = Storage('calendar.dat')
    credentials = storage.get()
    
    if credentials is None or credentials.invalid == True:
      print "Credenciais invalidas"
      credentials = run(FLOW, storage)
 
    
    http = httplib2.Http()
    http = credentials.authorize(http)

    
    service = build(serviceName='calendar', version='v3', http=http,
          developerKey=_developer_key) 
    
    return service

@login_required
def listar_eventos(request):

    service = authentic()
    
    events = service.events().list(calendarId='primary').execute()
    '''
    while True:
        for event in events['items']:
            print event['summary']
        page_token = events.get('nextPageToken')
        if page_token:
            events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        else:
            break
    '''
    return render_to_response('g_cal/welcome.html', {
                'events': events,
                })


@login_required
def listar_calendarios(request):
    
    service = authentic()
    calendar_list = service.calendarList().list().execute()

    return render_to_response('g_cal/lista_calendarios.html', {
            'agendas': calendar_list,
            })
    
@login_required
def novo_evento(request):
    
    service = authentic()
    event = {
      'summary': 'Titulo do Evento',
      'location': 'Bem aqui',
      'start': {
        'dateTime': '2012-08-15T10:00:00.000-07:00'
      },
      'end': {
        'dateTime': '2012-08-15T10:25:00.000-07:00'
      },
      'attendees': [
        {
          'email': 'rafael@sandrini.com.br',
          # Other attendee's data...
        },
        # ...
      ],
    }
    
    created_event = service.events().insert(calendarId='rafael@systembrasil.com.br', body=event).execute()

    return HttpResponseRedirect(reverse('g_cal:listar_eventos'))
    
    
    
@login_required
def deletar_evento(request):
    
    service = authentic()
    service.events().delete(calendarId='rafael@systembrasil.com.br', eventId='i9tssjfhkg35cunu6e1l1sbkr4').execute()

    return HttpResponseRedirect(reverse('g_cal:listar_eventos')) 
    
@login_required
def ver_evento(request):
    
    service = authentic()
    event = service.events().get(calendarId='rafael@systembrasil.com.br', eventId='vld5o7pkcc81d2t0bdp064un44').execute()

    return render_to_response('g_cal/ver_evento.html', {
            'event': event,
            })  
    
    
@login_required
def editar_evento(request):
    
    service = authentic()    
    
    # First retrieve the event from the API.
    event = service.events().get(calendarId='rafael@systembrasil.com.br', eventId='r99cfg3vbdmalbem7c09hh4qjg').execute()
    
    event['summary'] = 'ALTER TABLE!'

    updated_event = service.events().update(calendarId='rafael@systembrasil.com.br', eventId='r99cfg3vbdmalbem7c09hh4qjg', body=event).execute()
    
    return HttpResponseRedirect(reverse('g_cal:listar_eventos')) 


@login_required
def novo_calendario(request):
    
    service = authentic()     
    calendar = {
    'summary': 'NOVO CALENDARIO',
    'timeZone': 'America/Los_Angeles'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    return HttpResponseRedirect(reverse('g_cal:listar_calendarios')) 
    
@login_required
def deletar_calendario(request):
    
    service = authentic()     

    service.calendars().delete('systembrasil.com.br_vu6v2gpcssbk3cdso5jq5eecag').execute()  

    return HttpResponseRedirect(reverse('g_cal:listar_calendarios'))     
  
    
@login_required
def alterar_calendario(request):
    
    service = authentic()     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId='systembrasil.com.br_cljkoibfphr50q45etrb0fb8nc@group.calendar.google.com').execute()
    
    calendar['summary'] = 'NOME ALTERADO FILHO DA PUTA'
    
    updated_calendar = service.calendars().update(calendarId=calendar['systembrasil.com.br_cljkoibfphr50q45etrb0fb8nc@group.calendar.google.com'], body=calendar).execute()

    
    return HttpResponseRedirect(reverse('g_cal:listar_calendarios'))     
    
        
@login_required
def ver_calendario(request):
    
    service = authentic()     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId='systembrasil.com.br_cljkoibfphr50q45etrb0fb8nc@group.calendar.google.com').execute()
    
    return render_to_response('g_cal/ver_calendario.html', {
            'calendar': calendar,
            }) 
    
    