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

quarto_time_a = time_a.find(class_='period').get_text()
tempo_time_a = time_a.find(class_='time').get_text()
placar_time_a = time_a.find(class_='score-A x--bold').get_text()
placar_time_b = time_a.find(class_='score-B').get_text()
nome_time_a = time_a.find(class_='athlete-name')
indicador_time_a = time_a.find(class_='athlete-name')

print(quarto_time_a)
print(tempo_time_a)
print(placar_time_a)
print(placar_time_b)
print(nome_time_a)
print(indicador_time_a)


'''
dados = pd.DataFrame(
    {'Quarto': quarto,
     'Tempo': tempo,
     'Time_01': time_site,
     'Placar': placar,
     'Inf_2': acao_pessoa02
     })
'''

