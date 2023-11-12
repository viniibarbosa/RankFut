from django.shortcuts import render
import pytz
from datetime import datetime
import requests
import locale
from dotenv import load_dotenv
import os

def index(request):
    load_dotenv(override=True)
    api_key = os.getenv("API_KEY")
    id_campeonato = request.GET.get('campeonato')
    
    if(int(id_campeonato) == 2013):
        rodada = 34
    else:
        rodada = 13

    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')

    header = {f'X-Auth-Token' : api_key}
    resposta = requests.get(f'http://api.football-data.org/v4/competitions/{id_campeonato}/standings', headers=header)
    resposta_partidas = requests.get(f'http://api.football-data.org/v4/competitions/{id_campeonato}/matches?matchday={rodada}', headers=header)
    resposta_artilheiros = requests.get(f'http://api.football-data.org/v4/competitions/{id_campeonato}/scorers', headers=header)
    tabela= {}
    partidas = {}
    artilherios = {}
    
    rodadas = 10
    
    if(int(id_campeonato) == 2002):
        rodadas = 9
        
    
    
    if(resposta.status_code == 200 and resposta_partidas.status_code == 200 and resposta_artilheiros.status_code == 200):
        dados_api = resposta.json()
        partidas = resposta_partidas.json()
        artilherios = resposta_artilheiros.json()
    
        tabela = dados_api['standings'][0]['table']
        partidas = partidas['matches']
        artilherios = artilherios['scorers']
        fuso_horario_brasileiro = pytz.timezone('America/Sao_Paulo')

        for i in range(0,rodadas):
            data = datetime.fromisoformat(partidas[i]['utcDate']).astimezone(fuso_horario_brasileiro)
            partidas[i]['utcDate'] = data.strftime("%a %d/%m - %HH:%Mmin")
        
    return render(request, 'campeonatos.html', {'tabela': tabela, 'partidas':partidas, 'artilheiros': artilherios})

def menu_campeonatos(request):
    return render(request, 'menu-campeonatos.html')