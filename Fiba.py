import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException

r = requests.get('http://www.fiba.basketball/pt/basketballworldcup/2019/game/1409/Serbia-Czech-Republic')
soup = BeautifulSoup(r.content, 'html.parser')
jogada_jogada = soup.find(class_="selected-periods")

# enocntrar o primiero time
# por que estou separando por time?
# cada ação (jogada a jogada) o site não registra o time, mas sim a orgem visual no site, e no codigo está por
# <li class="action-item x--team-A"> ai como não consigo pegar essa informação eu estou separando os times e o inicio
# do jogo/quarto para depois organizar
# 1 - por quarto
# 2 - por tempo na quadra
time_a = jogada_jogada.find_all(class_="action-item x--team-A")

quarto_time_a = [a.find(class_='period').get_text() for a in time_a]
tempo_time_a = [a.find(class_='time').get_text() for a in time_a]
placar_time_b = [a.find(class_='score-B').get_text() for a in time_a]
placar_time_a = [a.find(class_='score-A').get_text() for a in time_a]
# como ele retorna com \n eu preciso tirar por ; e como são três eu preciso apenas escolher o do meio ai uso strip
acao = [a.find(class_="action").get_text() for a in time_a]
organizar01 = [item.replace(';', '') for item in acao]
organizar02 = [item.replace('\n', ';') for item in organizar01]
indicador = [item.strip(';') for item in organizar02]

dados = pd.DataFrame(
    {'Quarto': quarto_time_a,
     'Tempo': tempo_time_a,
     'Placar_casa': placar_time_a,
     'Placar_visitante': placar_time_b,
     'Inf_2': indicador
     })


saparar = dados["Inf_2"]

# separar nome e indicador
# lance livre
a1 = saparar.str.replace('2nd of 2 free throws made', '1/LL_Pts_C')
a2 = a1.str.replace('1st of 2 free throws missed', '1/LL_Pts_T')
a3 = a2.str.replace('2nd of 2 free throws missed', '1/LL_Pts_T')
a4 = a3.str.replace('1st of 2 free throws made', '1/LL_Pts_C')
a5 = a4.str.replace('1st free throw made', '1/LL_Pts_C')
a6 = a5.str.replace('1st free throw missed', '1/LL_Pts_T')
a7 = a6.str.replace('1st of 2 free throw made', '1/LL_Pts_C')
a8 = a7.str.replace('1/ 3 free throws awarded', '1/LL_Pts_T')
a9 = a8.str.replace('3rd of 3 free throws made', '1/LL_Pts_C')
a10 = a9.str.replace('2nd of 3 free throws made', '1/LL_Pts_C')
a11 = a10.str.replace('1st of 3 free throws made', '1/LL_Pts_C')
#dois pontos
a12 = a11.str.replace('2pt pullup jump shot missed', '1/2_Pts_T')
a13 = a12.str.replace('2pt pullup jump shot made', '1/2_Pts_C')
a14 = a13.str.replace('2pt fadeaway jump shot missed', '1/2_Pts_T')
a15 = a14.str.replace('2pt fadeaway jump shot made', '1/2_Pts_C')
a16 = a15.str.replace('2pt jump shot from center blocked', '1/2_Pts_T')
a17 = a16.str.replace('2pt jump shot from center missed', '1/2_Pts_T')
a18 = a17.str.replace('2pt jump shot from center made', '1/2_Pts_C')
a19 = a18.str.replace('2pt floating jump shot blocked', '1/2_Pts_T')
a20 = a19.str.replace('2pt floating jump shot missed', '1/2_Pts_T')
a21 = a20.str.replace('2pt floating jump shot made', '1/2_Pts_C')
a22 = a21.str.replace('2pt driving layup missed', '1/2_Pts_T')
a23 = a22.str.replace('2pt driving layup made', '1/2_Pts_C')
a24 = a23.str.replace('Arremesso de dois errado', '1/2_Pts_T')
a25 = a24.str.replace('Arremesso de dois certo', '1/2_Pts_C')
a26 = a25.str.replace('Bandeja Certa', '1/2_Pts_C')
a27 = a26.str.replace('Bandeja Errada', '1/2_Pts_T')
a28 = a27.str.replace('2pt driving layup blocked', '1/2_Pts_T')
a29 = a28.str.replace('2pt driving layup missed', '1/2_Pts_T')
a30 = a29.str.replace('2pt driving layup made', '1/2_Pts_C')
a31 = a30.str.replace('2pt hook shot missed', '1/2_Pts_T')
a32 = a31.str.replace('2pt hook shot made', '1/2_Pts_C')
a33 = a32.str.replace('2pt putback dunk missed', '1/2_Pts_T')
a34 = a33.str.replace('2pt putback dunk made', '1/2_Pts_C')
a35 = a34.str.replace('2pt jump shot blocked', '1/2_Pts_T')
a36 = a35.str.replace('2pt turnaround jump shot made', '1/2_Pts_C')
a37 = a36.str.replace('2pt turnaround jump shot missed', '1/2_Pts_T')
a38 = a37.str.replace('2pt Arr. Certo', '1/2_Pts_C')
a39 = a38.str.replace('2pt Arr. Errado', '1/2_Pts_T')
# três pontos
a40 = a39.str.replace('Arremesso de tres certo', '1/3_Pts_C')
a41 = a40.str.replace('Arremesso de tres errado', '1/3_Pts_T')
a42 = a41.str.replace('3pt jump shot from center missed', '1/3_Pts_T')
a43 = a42.str.replace('3pt jump shot from center made', '1/3_Pts_C')
a44 = a43.str.replace('3pt pullup jump shot missed', '1/3_Pts_T')
a45 = a44.str.replace('3pt pullup jump shot made', '1/3_Pts_C')
a46 = a45.str.replace('3pt step back jump shot missed', '1/3_Pts_T')
a47 = a46.str.replace('3pt step back jump shot made', '1/3_Pts_C')
a48 = a47.str.replace('3pt turnaround jump shot missed', '1/3_Pts_T')
a49 = a48.str.replace('3pt turnaround jump shot made', '1/3_Pts_C')
# rebotes
a50 = a49.str.replace('defensive rebound', '1/RD')
a51 = a50.str.replace('offensive rebound', '1/RO')
# recuperação de bola
a52 = a51.str.replace('steal', '1/BR')
# assistencias
a53 = a52.str.replace('made the assist', '1/AS')
#5 Faltas
a54 = a53.str.replace('unsportsmanlike foul 2 free throws awarded', '1/')
a55 = a54.str.replace('personal foul', '1/')
a56 = a55.str.replace(' 2 free throws awarded', '1/')
a57 = a56.str.replace(' 1 free throw awarded', '1/')
a58 = a57.str.replace('offensive foul', '1/')
a59 = a58.str.replace('technical foul', '1/')
a60 = a59.str.replace('foul drawn', '1/')
# substituição
a61 = a60.str.replace('Substitution in', '1/')
a62 = a61.str.replace('Substitution out', '1/')
# erros
a63 = a62.str.replace('turnover ball handling', '1/')
a64 = a63.str.replace('turnover travelling', '1/')
a65 = a64.str.replace('turnover bad pass', '1/')
a66 = a65.str.replace('turnover 3 seconds violation', '1/')
a67 = a66.str.replace('turnover out of bounds', '1/')
# tocos
a68 = a67.str.replace('blocked the shot', '1/')
# tempo técnico
a69 = a68.str.replace('Timeout', '1/')
# cravada
a70 = a69.str.replace('Enterrada', '1/')
# ponte aerea
a71 = a70.str.replace('Ponte Aerea Errada', '1/')
a72 = a71.str.replace('Ponte Aerea Certa', '1/')
# bola no alto
a73 = a72.str.replace('jump ball won', '1/')
a74 = a73.str.replace('jump ball situation throw-in', '1/')
# não sei
a75 = a74.str.replace('Tip In Errada', '1/')
a76 = a75.str.replace('Tip In Certa', '1/')
a77 = a76.str.replace('team ', '')
a78 = a77.str.replace('layup blocked', '1/')
a79 = a78.str.replace('free throw made', '1/')

dados['Nomes'] = a79
dados.drop('Inf_2', axis=1, inplace=True)
dados.to_csv("tabela_1.csv", index=None)



