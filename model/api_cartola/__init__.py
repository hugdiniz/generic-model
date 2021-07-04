import os
import numpy as np
import pandas as pd

import json
import logging

import requests
from requests.status_codes import codes
from requests.exceptions import HTTPError

import datetime



def parse_and_check_cartolafc(json_data: str) -> dict:
    try:
        data = json.loads(json_data)
        if 'game_over' in data and data['game_over']:
            logging.info('Desculpe-nos, o jogo acabou e não podemos obter os dados solicitados')
            raise CartolaFCGameOverError('Desculpe-nos, o jogo acabou e não podemos obter os dados solicitados')
        if 'mensagem' in data and data['mensagem']:
            logging.error(data['mensagem'])
            raise CartolaFCError(data['mensagem'].encode('utf-8'))
        return data
    except ValueError as error:
        logging.error('Error parsing and checking json data: %s', json_data)
        logging.error(error)
        raise CartolaFCOverloadError('Globo.com - Desculpe-nos, nossos servidores estão sobrecarregados.')

def mes_rodada(row,data_cartola):
    for mes in data_cartola:
        if row in data_cartola[mes]:
            return mes

def recuperar_info(parsed, fora_rodada):
    time = {}
    time['pts_capitao'] = 0
    time['qtd_gol'] = 0
    time['qtd_atleta_gol'] = 0
    ca = 0
    cv = 0
    for atleta in parsed['atletas']:

        if atleta['atleta_id'] == parsed['capitao_id']:
            time['pts_capitao'] =  atleta['pontos_num']

        try:
            time['qtd_gol'] += atleta['scout']['G']
            time['qtd_atleta_gol'] += 1
        except:
            time['qtd_gol'] += 0
            
        try:
            ca += atleta['scout']['CA']
            ca += 1
        except:
            ca += 0
            
        try:
            cv += atleta['scout']['CV']
            cv += 1
        except:
            cv += 0

    time['qtd_cartao'] = ca + (2*cv)
    time['pts_rodada'] = np.round(parsed['pontos'],2)
    time['time_id'] =  parsed['time']['time_id']
    time['Nome'] =  parsed['time']['nome_cartola']
    time['Time'] =  parsed['time']['nome']
    time['Rodada'] = parsed['rodada_atual']
    time['Patrimônio'] = parsed['patrimonio']
    time['url_escudo_png'] = parsed['time']['url_escudo_png']

    if fora_rodada:
        time['pts_capitao'] = 0
        time['qtd_gol'] = 0
        time['qtd_atleta_gol'] = 0
        time['qtd_cartao'] = 0
        time['pts_rodada'] = 0
        time['Patrimônio'] = 0    
    return time

def recuperar_info_parcial(parsed, atletas_parcial, fora_rodada):
    time = {}

    time['pts_capitao'] = 0
    time['qtd_gol'] = 0
    time['qtd_atleta_gol'] = 0

    ca = 0
    cv = 0
    pts_parcial = 0
    verificar_pts = True
    
    for atleta in parsed['atletas']:
        
        try:
            atleta_parc = atletas_parcial['atletas'][str(atleta['atleta_id'])]
            verificar_pts = True
        except: 
            verificar_pts= False
        
        if(verificar_pts):
            
            if atleta['atleta_id'] == parsed['capitao_id']:
                time['pts_capitao'] =  atleta_parc['pontuacao']
                pts_parcial += atleta_parc['pontuacao'] * 2
            else:
                pts_parcial += atleta_parc['pontuacao']  
            
            try:
                time['qtd_gol'] += atleta_parc['scout']['G']
                time['qtd_atleta_gol'] += 1
            except:
                time['qtd_gol'] += 0

            try:
                ca += atleta_parc['scout']['CA']
                ca += 1
            except:
                ca += 0

            try:
                cv += atleta_parc['scout']['CV']
                cv += 1
            except:
                cv += 0
   
    time['qtd_cartao'] = ca + (2*cv)
    time['pts_rodada'] = np.round(pts_parcial,2)
    time['time_id'] =  parsed['time']['time_id']
    time['Nome'] =  parsed['time']['nome_cartola']
    time['Time'] =  parsed['time']['nome']
    time['Rodada'] = atletas_parcial['rodada']
    time['Patrimônio'] = parsed['patrimonio']
    time['url_escudo_png'] = parsed['time']['url_escudo_png']
    
    
    if fora_rodada:
        time['pts_capitao'] = 0
        time['qtd_gol'] = 0
        time['qtd_atleta_gol'] = 0
        time['qtd_cartao'] = 0
        time['pts_rodada'] = 0
        time['Patrimônio'] = 0
    
    return time

def importar_api_cartola():
    data_cartola = {}
    data_cartola['Maio'] = [1]
    data_cartola['Junho'] = [2,3,4,5,6,7,8]
    data_cartola['Julho'] = [9,10,11,12,13]
    data_cartola['Agosto'] = [14,15,16,17,18]
    data_cartola['Setembro'] = [19,20,21,22]
    data_cartola['Outubro'] = [23,24,25,26,27,28,29]
    data_cartola['Novembro'] = [30,31,32,33,34,35,36]
    data_cartola['Dezembro'] = [37,38]


    lista_id_time = {
                        14922900 : 1,
                        3390328 : 1,
                        4754684 : 1,
                        14425978 : 1,
                        573044 : 1,
                        1244541 : 1,
                        14454639 : 1,
                        13969242 : 1,
                        1537719 : 1,
                        201715 : 1,
                        2630594 : 1,
                        1039148 : 1,
                        26080453 : 1,
                        29074871 : 1,
                        7251052 : 1,
                        17978418 : 1,
                        19712168 : 1,
                        25318016 : 1,
                        25593449 : 1,
                        28804167 : 1,
                        258287 : 1,
                        3395194 : 1,
                        18187532 : 1,
                        544869 : 1,

                    }

    todas_rodadas= False
    api_url = 'https://api.cartolafc.globo.com'
    url_mercado = '{api_url}/mercado/status'.format(api_url=api_url)
    url_atletas_parcial = '{api_url}/atletas/pontuados'.format(api_url=api_url)

    response_cartola = requests.get(url_mercado)
    try:
        cartola = parse_and_check_cartolafc(response_cartola.content.decode('utf-8'))
    except ValueError as error:        
        logging.error(error)
        return pd.DataFrame()
        
    

    app_openbar = pd.DataFrame()
    e_parcial = False
    if( cartola['status_mercado'] == 2):
        
        print('-------Resultado Parcial--------')

        rodadas = range(1,cartola['rodada_atual']+1)
        rodada_parcial = rodadas[-1]
        
        response_parcial = requests.get(url_atletas_parcial)
        atletas_pts_parcial = parse_and_check_cartolafc(response_parcial.content.decode('utf-8'))
        
        times = []
        for id_time in lista_id_time:

            fora_rodada = True
            if lista_id_time[id_time] <= rodada_parcial:
                fora_rodada = False
                
            url_parcial = '{api_url}/time/id/{id_time}/{num_rodada}'.format(api_url=api_url, id_time=id_time, num_rodada=rodada_parcial)
            response_time_parcial = requests.get(url_parcial)
            parsed = parse_and_check_cartolafc(response_time_parcial.content.decode('utf-8'))
        
            times.append(recuperar_info_parcial(parsed, atletas_pts_parcial, fora_rodada))
        
        dados = pd.DataFrame(times, columns=['time_id','Nome','Time','Rodada','pts_rodada','pts_capitao','qtd_gol',
                                            'qtd_atleta_gol','qtd_cartao','Patrimônio','url_escudo_png'])

        dados = dados.sort_values(['pts_rodada','pts_capitao','qtd_gol','qtd_atleta_gol','qtd_cartao','Patrimônio'], ascending=[False, False, False, False, True, False])
        dados['Colocação'] = np.arange(1,dados.shape[0]+1)
        dados['Mês'] = dados['Rodada'].apply(lambda x: mes_rodada(x,data_cartola))

        rodada = dados.filter(items=['time_id','Nome','Time','Mês','Rodada','Colocação','pts_rodada','pts_capitao','qtd_gol','qtd_atleta_gol','qtd_cartao','Patrimônio'])
        rodada.to_csv(f'Rodada Parcial {rodada_parcial}.csv', index=False)
        app_openbar = pd.concat([app_openbar,rodada])
        
        e_parcial = True
        print('-------Fim--------')
            
    else:
        print('-------Resultado Final--------')
        
        if(todas_rodadas):
            rodadas = range(1,cartola['rodada_atual'])
        else:
            rodadas = range(cartola['rodada_atual']-1,cartola['rodada_atual'])
                
            
        for num_rodada in rodadas:
            times = []
            for id_time in lista_id_time:

                fora_rodada = True
                if lista_id_time[id_time] <= num_rodada:
                    fora_rodada = False

                url = '{api_url}/time/id/{id_time}/{num_rodada}'.format(api_url=api_url, id_time=id_time, num_rodada=num_rodada)
                response = requests.get(url)
                parsed = parse_and_check_cartolafc(response.content.decode('utf-8'))

                times.append(recuperar_info(parsed,fora_rodada))


            dados = pd.DataFrame(times, columns=['time_id','Nome','Time','Rodada','pts_rodada','pts_capitao','qtd_gol',
                                                'qtd_atleta_gol','qtd_cartao','Patrimônio','url_escudo_png'])

            dados = dados.sort_values(['pts_rodada','pts_capitao','qtd_gol','qtd_atleta_gol','qtd_cartao','Patrimônio'], ascending=[False, False, False, False, True, False])
            dados['Colocação'] = np.arange(1,dados.shape[0]+1)
            dados['Mês'] = dados['Rodada'].apply(lambda x: mes_rodada(x,data_cartola))

            rodada = dados.filter(items=['time_id','Nome','Time','Mês','Rodada','Colocação','pts_rodada','pts_capitao','qtd_gol','qtd_atleta_gol','qtd_cartao','Patrimônio'])
            rodada.to_csv(f'Rodada Final {num_rodada}.csv', index=False)
            app_openbar = pd.concat([app_openbar,rodada])
            print('-------Fim--------')


    return app_openbar,e_parcial  