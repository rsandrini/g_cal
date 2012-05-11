from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import httplib2

'''
@author: Rafael Sandrini Santos
@version: 0.1 2012-05-10

Metodo de listar eventos do calendario principal GOOGLE API CALENDAR 3.0
Altere os dados de cliente_id, cliente_secret e developer_key
No primeiro acesso sera aberto uma nova aba/janela para autorizacao 
de acesso ao google Calendar. isto e conhecido como "consentimento do usuario"
Basta selecionar que autoriza... O token e trocado automaticamente e ele deve
mostrar uma lista com as tarefas da agenda principal.
'''

@login_required
def listar_eventos(request):

    FLOW = OAuth2WebServerFlow(
        client_id='SEU_ID_CLIENTE',
        client_secret='SUA_SECRET_CLIENT',
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
          developerKey="SUA_API_KEY") 
    
    events = service.events().list(calendarId='primary').execute()
    
    while True:
        for event in events['items']:
            print event['summary']
        page_token = events.get('nextPageToken')
        if page_token:
            events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        else:
            break
      
    return render_to_response('g_cal/welcome.html', {
                'events': events,
                })

