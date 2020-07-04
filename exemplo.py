import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException
import urllib
import re

r = requests.get('http://www.fiba.basketball/pt/basketballworldcup/2019/games')
soup = BeautifulSoup(r.content, 'html.parser')
inf = soup.find_all(class_="latest_qualifier_games")

inf2 = [a['href'] for a in soup.find_all('a', href=True)]
inf3 = pd.DataFrame({'inf2': inf2})

tamano = len(inf3)
NomeA = str('http://www.fiba.basketball')
Atime = [NomeA for item in range(0, tamano)]
inf3['inf4'] = Atime

inf3['nomedanovacoluna'] = inf3.inf4.str.cat(inf3.inf2)
inf3.drop('inf4', axis=1, inplace=True)
inf3.drop('inf2', axis=1, inplace=True)

p2_site = inf3.loc[inf3.nomedanovacoluna.str.contains('http://www.fiba.basketball/pt/basketballworldcup/2019/game/', regex=True)]

########################################################################################################################
#lista = p2_site.values.tolist()
#lista.translate[remove_punctuation(i) for i in train_pos]
#print(lista)

colunas = ['coluna1', 'coluna2', 'coluna3']

for i in p2_site.nomedanovacoluna.values:
    ii = 0
    geral_informacoes = []
    r = requests.get(f'{i}')
    soup_site = BeautifulSoup(r.content, 'html.parser')

    # encontrar o nome dos times
    # ai da para fazer uma tabela geral
    inf_da_partida = soup_site.find_all(class_="header-scores_desktop")

    inf_nome_A = inf_da_partida[0].find(class_='team-A')
    NomeA = inf_nome_A.find(class_='team-name').get_text()

    inf_nome_B = inf_da_partida[0].find(class_='team-B')
    NomeB = inf_nome_B.find(class_='team-name').get_text()

    inf_placar_A = inf_da_partida[0].find(class_='score-A').get_text()
    inf_placar_B = inf_da_partida[0].find(class_='score-B').get_text()

    inf_local = inf_da_partida[0].find(class_='location').get_text()

    # fazer uma lista e depois um for para acrescentar a cada loop que fizer
    informacoes = [NomeA, inf_placar_A, NomeB, inf_placar_B, inf_local]
    print(informacoes)
    # encontrar o nome dos times
    # ai da para fazer uma tabela geral
    inf = soup_site.find_all(class_="header-scores_desktop")
    infA = inf[0].find(class_='team-A')
    NomeA = infA.find(class_='team-name').get_text()
    infB = inf[0].find(class_='team-B')
    NomeB = infB.find(class_='team-name').get_text()

    ########################################################################################################################
    jogada_jogada = soup_site.find(class_="selected-periods")
    # enocntrar o primiero time
    # por que estou separando por time?
    # cada ação (jogada a jogada) o site não registra o time, mas sim a orgem visual no site, e no codigo está por
    # <li class="action-item x--team-A"> ai como não consigo pegar essa informação eu estou separando os times e o inicio
    # do jogo/quarto para depois organizar
    # 1 - por quarto
    # 2 - por tempo na quadra
    time_a = jogada_jogada.find_all(class_="action-item x--team-A")
    Aquarto_time_a = [a.find(class_='period').get_text() for a in time_a]
    Atempo_time_a = [a.find(class_='time').get_text() for a in time_a]
    Aplacar_time_b = [a.find(class_='score-B').get_text() for a in time_a]
    Aplacar_time_a = [a.find(class_='score-A').get_text() for a in time_a]
    # como ele retorna com \n eu preciso tirar por ; e como são três eu preciso apenas escolher o do meio ai uso strip
    Aacao = [a.find(class_="action").get_text() for a in time_a]
    Aorganizar01 = [item.replace(';', '') for item in Aacao]
    Aorganizar02 = [item.replace('\n', ';') for item in Aorganizar01]
    Aindicador = [item.strip(';') for item in Aorganizar02]
    Atime = [NomeA for item in Aindicador]

    dadosA = pd.DataFrame(
        {'Quarto': Aquarto_time_a,
         'Tempo': Atempo_time_a,
         'Time': Atime,
         'Placar_casa': Aplacar_time_a,
         'Placar_visitante': Aplacar_time_b,
         'Inf_2': Aindicador
         })
    ########################################################################################################################
    time_b = jogada_jogada.find_all(class_="action-item x--team-B")
    Bquarto_time_a = [a.find(class_='period').get_text() for a in time_b]
    Btempo_time_a = [a.find(class_='time').get_text() for a in time_b]
    Bplacar_time_b = [a.find(class_='score-B').get_text() for a in time_b]
    Bplacar_time_a = [a.find(class_='score-A').get_text() for a in time_b]
    # como ele retorna com \n eu preciso tirar por ; e como são três eu preciso apenas escolher o do meio ai uso strip
    Bacao = [a.find(class_="action").get_text() for a in time_b]
    Borganizar01 = [item.replace(';', '') for item in Bacao]
    Borganizar02 = [item.replace('\n', ';') for item in Borganizar01]
    Bindicador = [item.strip(';') for item in Borganizar02]
    Btime = [NomeB for item in Bindicador]

    dadosB = pd.DataFrame(
        {'Quarto': Bquarto_time_a,
         'Tempo': Btempo_time_a,
         'Time': Btime,
         'Placar_casa': Bplacar_time_a,
         'Placar_visitante': Bplacar_time_b,
         'Inf_2': Bindicador
         })

    juntar_dados = pd.concat([dadosA, dadosB], axis=0)
    # mudar o OT =  prorrogação por T para deixar na em uma ordem dos tempos (primeiro vem O depois Q no alfabeto)
    juntar_dados["Quarto"] = juntar_dados["Quarto"].str.replace('OT', 'T')
    # ordena eles
    dados = juntar_dados.sort_values(['Quarto', 'Tempo'])

    saparar = dados["Inf_2"]

    # separar nome e indicador
    # lance livre
    a1 = saparar.str.replace('2nd of 2 free throws made', '9/LL_Pts_C')
    a2 = a1.str.replace('1st of 2 free throws missed', '9/LL_Pts_T')
    a3 = a2.str.replace('2nd of 2 free throws missed', '9/LL_Pts_T')
    a4 = a3.str.replace('1st of 2 free throws made', '9/LL_Pts_C')
    a5 = a4.str.replace('1st free throw made', '9/LL_Pts_C')
    a6 = a5.str.replace('1st free throw missed', '9/LL_Pts_T')
    a7 = a6.str.replace('1st of 2 free throw made', '9/LL_Pts_C')
    a8 = a7.str.replace('1/ 3 free throws awarded', '9/LL_Pts_T')
    a9 = a8.str.replace('3rd of 3 free throws made', '9/LL_Pts_C')
    a10 = a9.str.replace('2nd of 3 free throws made', '9/LL_Pts_C')
    a11 = a10.str.replace('1st of 3 free throws made', '9/LL_Pts_C')
    # dois pontos
    a12 = a11.str.replace('2pt pullup jump shot missed', '9/2_Pts_T')
    a13 = a12.str.replace('2pt pullup jump shot made', '9/2_Pts_C')
    a14 = a13.str.replace('2pt fadeaway jump shot missed', '9/2_Pts_T')
    a15 = a14.str.replace('2pt fadeaway jump shot made', '9/2_Pts_C')
    a16 = a15.str.replace('2pt jump shot from center blocked', '9/2_Pts_T')
    a17 = a16.str.replace('2pt jump shot from center missed', '9/2_Pts_T')
    a18 = a17.str.replace('2pt jump shot from center made', '9/2_Pts_C')
    a19 = a18.str.replace('2pt floating jump shot blocked', '9/2_Pts_T')
    a20 = a19.str.replace('2pt floating jump shot missed', '9/2_Pts_T')
    a21 = a20.str.replace('2pt floating jump shot made', '9/2_Pts_C')
    a22 = a21.str.replace('2pt driving layup missed', '9/2_Pts_T')
    a23 = a22.str.replace('2pt driving layup made', '9/2_Pts_C')
    a24 = a23.str.replace('Arremesso de dois errado', '9/2_Pts_T')
    a25 = a24.str.replace('Arremesso de dois certo', '9/2_Pts_C')
    a26 = a25.str.replace('Bandeja Certa', '9/2_Pts_C')
    a27 = a26.str.replace('Bandeja Errada', '9/2_Pts_T')
    a28 = a27.str.replace('2pt driving layup blocked', '9/2_Pts_T')
    a29 = a28.str.replace('2pt driving layup missed', '9/2_Pts_T')
    a30 = a29.str.replace('2pt driving layup made', '9/2_Pts_C')
    a31 = a30.str.replace('2pt hook shot missed', '9/2_Pts_T')
    a32 = a31.str.replace('2pt hook shot made', '9/2_Pts_C')
    a33 = a32.str.replace('2pt putback dunk missed', '9/2_Pts_T')
    a34 = a33.str.replace('2pt putback dunk made', '9/2_Pts_C')
    a35 = a34.str.replace('2pt jump shot blocked', '9/2_Pts_T')
    a36 = a35.str.replace('2pt turnaround jump shot made', '9/2_Pts_C')
    a37 = a36.str.replace('2pt turnaround jump shot missed', '9/2_Pts_T')
    a38 = a37.str.replace('2pt Arr. Certo', '9/2_Pts_C')
    a39 = a38.str.replace('2pt Arr. Errado', '9/2_Pts_T')
    # três pontos
    a40 = a39.str.replace('Arremesso de tres certo', '9/3_Pts_C')
    a41 = a40.str.replace('Arremesso de tres errado', '9/3_Pts_T')
    a42 = a41.str.replace('3pt jump shot from center missed', '9/3_Pts_T')
    a43 = a42.str.replace('3pt jump shot from center made', '9/3_Pts_C')
    a44 = a43.str.replace('3pt pullup jump shot missed', '9/3_Pts_T')
    a45 = a44.str.replace('3pt pullup jump shot made', '9/3_Pts_C')
    a46 = a45.str.replace('3pt step back jump shot missed', '9/3_Pts_T')
    a47 = a46.str.replace('3pt step back jump shot made', '9/3_Pts_C')
    a48 = a47.str.replace('3pt turnaround jump shot missed', '9/3_Pts_T')
    a49 = a48.str.replace('3pt turnaround jump shot made', '9/3_Pts_C')
    # rebotes
    a50 = a49.str.replace('defensive rebound', '9/RD')
    a51 = a50.str.replace('offensive rebound', '9/RO')
    # recuperação de bola
    a52 = a51.str.replace('steal', '9/BR')
    # assistencias
    a53 = a52.str.replace('made the assist', '9/AS')
    # 5 Faltas
    a54 = a53.str.replace('unsportsmanlike foul 2 free throws awarded', '9/FC_A')
    a55 = a54.str.replace('personal foul', '9/FC')
    a56 = a55.str.replace(' 2 free throws awarded', '')
    a57 = a56.str.replace(' 1 free throw awarded', '')
    a58 = a57.str.replace('offensive foul', '9/FC_O')
    a59 = a58.str.replace('technical foul', '9/FC_T')
    a60 = a59.str.replace('foul drawn', '9/FR')
    # substituição
    a61 = a60.str.replace('Substitution in', '9/substituicao_entra')
    a62 = a61.str.replace('Substitution out', '9/substituicao_sai')
    # erros
    a63 = a62.str.replace('turnover ball handling', '9/ER')
    a64 = a63.str.replace('turnover travelling', '9/ER')
    a65 = a64.str.replace('turnover bad pass', '9/ER')
    a66 = a65.str.replace('turnover 3 seconds violation', '9/ER')
    a67 = a66.str.replace('turnover out of bounds', '9/ER')
    # tocos
    a68 = a67.str.replace('blocked the shot', '9/TO')
    # tempo técnico
    a69 = a68.str.replace('Timeout', '9/tempo_tecnico')
    # cravada
    a70 = a69.str.replace('Enterrada', '9/EN')
    # ponte aerea
    a71 = a70.str.replace('Ponte Aerea Errada', '9/EN_T')
    a72 = a71.str.replace('Ponte Aerea Certa', '9/EN')
    # bola no alto
    a73 = a72.str.replace('jump ball won', '9/inicio_quarto')
    a74 = a73.str.replace('jump ball situation throw-in', '9/muda_bola')
    # não sei
    a75 = a74.str.replace('Tip In Errada', '9/2_Pts_T')
    a76 = a75.str.replace('Tip In Certa', '9/2_Pts_C')
    a77 = a76.str.replace('team ', '')
    a78 = a77.str.replace('layup blocked', '9/2_Pts_T')
    a79 = a78.str.replace('free throw made', '9/LL_Pts_T')
    a80 = a79.str.replace('turnover', '9/ER')
    a81 = a80.str.replace('2pt step back jump shot made', '9/2_Pts_C')
    a82 = a81.str.replace('2pt step back jump shot missed', '9/2_Pts_T')
    a83 = a82.str.replace('2pt step back jump shot blocked', '9/2_Pts_T')
    a84 = a83.str.replace('2pt jump shot inside the paint missed', '9/2_Pts_T')
    a85 = a84.str.replace('2pt jump shot inside the paint made', '9/2_Pts_C')
    a86 = a85.str.replace(' 3 free throws awarded', '')

    a87 = a86.str.replace('2nd of 3 free throws missed', '9/LL_Pts_T')
    a88 = a87.str.replace('3nd of 3 free throws missed', '9/LL_Pts_T')
    a89 = a88.str.replace('1nd of 3 free throws missed', '9/LL_Pts_T')
    a90 = a89.str.replace('3rd of 3 free throws missed', '9/LL_Pts_T')
    a91 = a90.str.replace('1st of 3 free throws missed', '9/LL_Pts_T')
    a92 = a91.str.replace(' 5 seconds violation', '')
    a93 = a92.str.replace('24 seconds violation', '')
    a94 = a93.str.replace('2pt hook shot blocked', '9/2_Pts_T')
    a95 = a94.str.replace('1st of 1 ', '')

    # nome;1/indicador
    # estou fazendo isso pq tem indicadores que não tem jogadores(noomes)
    # quando coloco 1 ele ajuda a separa os dois e deixar uma variável 1 quando não tem nome
    # depois eu tiro esse ;1 e coloco um identificador do time
    mudados_00 = a95.str.split('/')
    mudados_01 = mudados_00.str.get(1)
    dados['Indicador'] = mudados_01

    mudados_02 = mudados_00.str.get(0)
    mudados_03 = mudados_02.str.replace('9', '')
    mudados_04 = mudados_03.str.replace(';', '')
    dados['Nome'] = mudados_04

    dados.drop('Inf_2', axis=1, inplace=True)
    dados.to_csv("tabela_1.csv", index=None)
    dados.to_csv(f"./Dados03/tabela_{ii}.csv", index=None)
    ii = ii + 1
