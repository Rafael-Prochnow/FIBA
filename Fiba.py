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
acao = [a.find(class_="action") for a in time_a]
indicador = [item.find(class_='action-description').get_text() for item in acao]

nome = [item.find(class_='athlete-name').get_text() for item in acao]
# indicador = [item.replace('\n', ';') for item in organizar01]
# indicador = [item.strip(';') for item in organizar01]

# print(indicador)

# duplica a coluna e faz uma coluna que use inidcador e

dados = pd.DataFrame(
    {'Quarto': quarto_time_a,
     'Tempo': tempo_time_a,
     'Placar_casa': placar_time_a,
     'Placar_visitante': placar_time_b,
     'Inf_2': indicador
     })
# separar nome e indicador

#dados['Nomes'] = nome

dados.to_csv("tabela_1.csv", index=None)


