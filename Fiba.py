import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException

r = requests.get('http://www.fiba.basketball/pt/basketballworldcup/2019/game/1409/EUA-Pol%c3%b4nia')
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
organizar01 = [item.replace('\n', ';') for item in acao]
indicador = [item.strip(';') for item in organizar01]

dados = pd.DataFrame(
    {'Quarto': quarto_time_a,
     'Tempo': tempo_time_a,
     'Placar_casa': placar_time_a,
     'Placar_visitante': placar_time_b,
     'Inf_2': indicador
     })


print(dados)

# separar nome e indicador
# lance livre
a1 = .str.replace('2nd of 2 free throws made', '1,')
a2 = a1.str.replace('1st of 2 free throws missed', '1,')
a3 = a2.str.replace('2nd of 2 free throws missed', '1,')
a4 = a3.str.replace('1st of 2 free throws made', '1,')
a5 = a4.str.replace('1st free throw made', '1,')
a6 = a5.str.replace('1st free throw missed', '1,')
#dois pontos
a7 = a6.str.replace('2pt pullup jump shot missed', '1,')
a8 = a7.str.replace('2pt fadeaway jump shot made', '1;')
a9 = a8.str.replace('2pt jump shot from center missed', '1,')
a10 = a9.str.replace('2pt jump shot from center made', '1,')
a11 = a10.str.replace('2pt floating jump shot missed', '1,')
a12 = a11.str.replace('2pt driving layup missed', '1,')
a13 = a12.str.replace('Arremesso de dois certo', '1,')
a14 = a13.str.replace('Bandeja Certa', '1,')
a15 = a14.str.replace('2pt driving layup made', '1,')
a16 = a15.str.replace('layup blocked', '1,')
a17 = a16.str.replace('Arremesso de dois errado', '1,')
a18 = a17.str.replace('2pt hook shot missed', '1,')
a19 = a18.str.replace('Bandeja Errada', '1,')
a20 = a19.str.replace('2pt floating jump shot made', '1,')
# três pontos
a21 = a20.str.replace('Arremesso de tres certo', '1,')
a22 = a21.str.replace('Arremesso de tres errado', '1,')
a23 = a22.str.replace('3pt jump shot from center missed', '1,')
a24 = a23.str.replace('3pt pullup jump shot missed', '1,')
a25 = a24.str.replace('3pt jump shot from center made', '1,')
a26 = a25.str.replace('3pt step back jump shot missed', '1,')
a27 = a26.str.replace('3pt pullup jump shot made', '1,')
# rebotes
a28 = a27.str.replace('defensive rebound', '1,')
a29 = a28.str.replace('team offensive rebound', '1,')
a30 = a29.str.replace('team defensive rebound', '1,')
a31 = a30.str.replace('offensive rebound', '1,')
# recuperação de bola
a32 = a31.str.replace('steal', '1,')
# assistencias
a33 = a32.str.replace('made the assist', '1,')
# Faltas
a34 = a33.str.replace('foul drawn', '1,')
a35 = a34.str.replace('personal foul', '1,')
a36 = a35.str.replace('offensive foul', '1,')
a37 = a36.str.replace('technical foul', '1,')
# substituição
a38 = a37.str.replace('Substitution in', '1,')
a39 = a38.str.replace('Substitution out', '1,')
# erros
a40 = a39.str.replace('turnover', '1,')
# tocos
a41 = a40.str.replace('blocked the shot', '1,')
# tempo técnico
a42 = a41.str.replace('Timeout', '1,')
# cravada
a43 = a42.str.replace('Enterrada', '1,')
# ponte aerea
a44 = a43.str.replace('Ponte Aerea Errada', '1,')
a45 = a44.str.replace('Ponte Aerea Certa', '1,')
# bola no alto
a46 = a45.str.replace('jump ball won', '1,')
a47 = a46.str.replace('jump ball situation', '1,')
# não sei
a48 = a47.str.replace('Tip In Errada', '1,')
a49 = a48.str.replace('Tip In Certa', '1,')


# indicador = [item.replace('\n', ';') for item in organizar01]
# indicador = [item.strip(';') for item in organizar01]

# print(indicador)

# duplica a coluna e faz uma coluna que use inidcador e



#dados['Nomes'] = nome

dados.to_csv("tabela_1.csv", index=None)
'''

