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
import gflags

from django.template import RequestContext

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
    FLAGS = gflags.FLAGS
    # Configure um objeto de fluxo para ser utilizado se precisa autenticar. este
    # Exemplo usa OAuth 2.0, e montamos o OAuth2WebServerFlow com
    # Informações de que necessita para autenticar. Note-se que é chamado
    # Fluxo Servidor Web, mas também pode lidar com o fluxo para o nativo
    # Aplicações
    # O client_id e client_secret são copiados a partir do separador Acesso API em
    # O Google APIs Console
    FLOW = OAuth2WebServerFlow(
    client_id=_cliente_id,
    client_secret=_cliente_secret,
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='SS-Google/1.0') # Nome e versão da aplicação e não da API google
    # Para desativar o recurso de servidor local, descomente a seguinte linha:
    #FLAGS.auth_local_webserver = False


    # Se as credenciais não existem ou são inválidas, executado através do cliente nativo
    # Fluxo. O objeto de armazenamento irá garantir que, se bem sucedida a boa Credenciais 
    # vai ficar gravado de volta para um arquivo

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
def listar_eventos(request, calendario_id):
    service = authentic()
    events = service.events().list(calendarId=calendario_id).execute()
    return render_to_response('g_cal/listar_eventos.html', {
                'events': events, 'calendario_id': calendario_id,
                })


@login_required
def listar_calendarios(request):
    service = authentic()
    calendar_list = service.calendarList().list().execute()
    return render_to_response('g_cal/lista_calendarios.html', {
            'agendas': calendar_list,
            })
    
@login_required
def novo_evento(request, calendario_id):
    action = '/g_cal/'+calendario_id+'/novo_evento/'
    service = authentic()

    if request.POST:
        
        service = authentic()    

        

            #debug
            print event
        
            created_event = service.events().insert(calendarId=calendario_id, body=event).execute()
            return HttpResponseRedirect('/g_cal/'+calendario_id+'/listar_eventos') 
    
    
    else:
        calendar = service.calendars().get(calendarId=calendario_id).execute()
        return render_to_response('g_cal/form_evento.html',
                              {'action':action, 'calendar':calendar}, 
                              context_instance=RequestContext(request))
    
    

'''
Recebe a ID de uma calendario e o ID de um evento que será deletado
retorna para lista de eventos
'''    
@login_required
def deletar_evento(request, calendario_id, evento_id):
    
    service = authentic()
    service.events().delete(calendarId=calendario_id, eventId=evento_id).execute()

    return HttpResponseRedirect(reverse('g_cal:listar_eventos', args=[calendario_id])) 
    
@login_required
def ver_evento(request, calendario_id, evento_id):
    
    service = authentic()
    event = service.events().get(calendarId=calendario_id, eventId=evento_id).execute()

    return render_to_response('g_cal/ver_evento.html', {
            'event': event, 'calendario_id':calendario_id,
            })    
    
@login_required
def editar_evento(request, calendario_id, evento_id):
    action = '/g_cal/'+calendario_id+'/editar_evento'
    
    if request.POST:
    
        service = authentic()    
        
        # First retrieve the event from the API.
        event = service.events().get(calendarId=calendario_id, eventId=evento_id).execute()
        
        event['summary'] = 'Evento geneticamente modificado'
    
        updated_event = service.events().update(calendarId=calendario_id, eventId=evento_id, body=event).execute()
        
        return HttpResponseRedirect('/g_cal/'+calendario_id+'/listar_eventos') 
    else:
        return render_to_response('g_cal/form_evento.html',
                              {'action':action}, 
                              context_instance=RequestContext(request))


@login_required
def novo_calendario(request):
    
    service = authentic()     
    calendar = {
    'summary': 'NOVO CALENDARIO',
    'timeZone': 'America/Sao_Paulo'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    return HttpResponseRedirect(reverse('g_cal:listar_calendarios')) 
    
@login_required
def deletar_calendario(request, calendario_id):
    
    service = authentic()     

    service.calendars().delete(calendario_id).execute()  

    return HttpResponseRedirect(reverse('g_cal:listar_calendarios'))     
  
    
@login_required
def alterar_calendario(request, calendario_id):
    
    service = authentic()     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId=calendario_id).execute()
    
    calendar['summary'] = 'Nome do calendario HFC'
    
    updated_calendar = service.calendars().update(calendarId=calendario_id, body=calendar).execute()

    
    return HttpResponseRedirect(reverse('g_cal:listar_calendarios'))     
    
        
@login_required
def ver_calendario(request, calendario_id):
    
    service = authentic()     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId=calendario_id).execute()
    
    return render_to_response('g_cal/ver_calendario.html', {
            'calendar': calendar,
            }) 

@login_required
def ver_calendario_g(request, calendario_id):
    
    service = authentic()     
    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId=calendario_id).execute()
    
    return render_to_response('g_cal/ver_calendario_g.html', {
            'calendar': calendar,
            }) 

@login_required
def vincular_pessoa_calendario(request, calendario_id):
    service = authentic()
    
    rule = {
        'role':'writer',
        'scope':
        {
            'type':'user',
            'value':'alyson@systembrasil.com.br',
        },
    }
    
    created_rule = service.acl().insert(calendarId=calendario_id, body=rule).execute()
    
    return HttpResponseRedirect(reverse('g_cal:listar_calendarios'))  
    
    
def montar_evento(request):
    dateTimeBegin = ""
        dateTimeEnd = ""
        rep_freq = ""
        
        if request.POST.get("dia_todo") == None:
            dateTimeBegin = request.POST.get("dt_inicio")+'T'+request.POST.get("hr_inicio")+'.000-03:00'
            # O evento recebe a data de inicio para fim pois provavelmente irá terminar no mesmo dia...
            dateTimeEnd = request.POST.get("dt_inicio")+'T'+request.POST.get("hr_fim")+'.000-03:00'
        else:
            dateTimeEnd = dateTimeBegin = request.POST.get("dt_inicio")

        
        if request.POST.get("cbo_repeticao") == "unico":
            event = {
             'summary': request.POST.get("titulo"),
             'description': request.POST.get("descricao"),
    
             'location': 'localizacao',
             'start': {
               'dateTime':  dateTimeBegin,
               'timeZone': 'America/Sao_Paulo'
             },
             'end': {
               'dateTime': dateTimeEnd,
               'timeZone': 'America/Sao_Paulo'
             },

             'attendees': [
               {
                 'email': 'rafael@systembrasil.com.br',
                 # Other attendee's data...
               },
               # ...
             ],
            }
        
        else:
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
                dias_semana = "SU,"
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
                
            # Numero para definir a cada quantos X ele vai pular para o proximo evento #capeta    
            rep_a_cada = request.POST.get("rep_a_cada")
                
            #verifica se existe repetição em numero de ocorrencias
            if request.POST.get("tm_ocorrencias"):
                repeticao_vezes = request.POST.get("tm_ocorrencias")
                
                event = {
                 'summary': request.POST.get("titulo"),
                 'description': request.POST.get("descricao"),
        
                 'location': 'localizacao',
                 'start': {
                   'dateTime':  dateTimeBegin,
                   'timeZone': 'America/Sao_Paulo'
                 },
                 'end': {
                   'dateTime': dateTimeEnd,
                   'timeZone': 'America/Sao_Paulo'
                 },
                 'recurrence': [
                   'RRULE:FREQ='+rep_freq+';COUNT='+repeticao_vezes+';BYDAY='+dias_semana+";INTERVAL="+intervalo_n,
                 ],
                 'attendees': [
                   {
                     'email': 'rafael@sandrini.com.br',
                     # Other attendee's data...
                   },
                   # ...
                 ],
                }
                
                
            elif request.POST.get("tm_sempre"):
                # remove a data de termino
                event = {
                 'summary': request.POST.get("titulo"),
                 'description': request.POST.get("descricao"),
        
                 'location': 'localizacao',
                 'start': {
                   'dateTime':  dateTimeBegin,
                   'timeZone': 'America/Sao_Paulo'
                 },
                 'end': {
                   'dateTime': dateTimeEnd,
                   'timeZone': 'America/Sao_Paulo'
                 },
                 'recurrence': [
                   'RRULE:FREQ='+rep_freq+';BYDAY='+dias_semana+";INTERVAL="+intervalo_n,
                 ],
                 'attendees': [
                   {
                     'email': 'rafael@sandrini.com.br',
                     # Other attendee's data...
                   },
                   # ...
                 ],
                }
                
            elif request.POST.get("dt_fim"):
                #Determina o UNTIL
                dt_fim = request.POST.get("dt_fim")
                event = {
                 'summary': request.POST.get("titulo"),
                 'description': request.POST.get("descricao"),
        
                 'location': 'localizacao',
                 'start': {
                   'dateTime':  dateTimeBegin,
                   'timeZone': 'America/Sao_Paulo'
                 },
                 'end': {
                   'dateTime': dateTimeEnd,
                   'timeZone': 'America/Sao_Paulo'
                 },
                 'recurrence': [
                   'RRULE:FREQ='+rep_freq+';UNTIL='+dt_fim+';BYDAY='+dias_semana+";INTERVAL="+intervalo_n,
                 ],
                 'attendees': [
                   {
                     'email': 'rafael@sandrini.com.br',
                     # Other attendee's data...
                   },
                   # ...
                 ],
                }
                
        return event    
    
@login_required
def listar_acl_calendario(request, calendario_id):
    service = authentic()
    acl = service.acl().list(calendarId=calendario_id).execute()
    
    
    return render_to_response('g_cal/listar_acl_calendario.html', {
        'acl': acl,
    }) 
  
    
    
    