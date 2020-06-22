import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos')
soup = BeautifulSoup(r.content, 'html.parser')

# 3 encontra o time, está separado dos demais
items02 = soup.find_all(class_='large-10 small-8 medium-10 columns move_action_content move_action_content_one')
time_site = [nome_time.find('p').get_text() for nome_time in items02]
# passa para primeira inf encontra quarto tempo placar
items = soup.find_all(class_='large-2 small-4 medium-2 columns move_action_time')
quarto = [nome_quarto.find(class_='quarter').get_text() for nome_quarto in items]
tempo = [nome_tempo.find(class_='time').get_text() for nome_tempo in items]
placar = [nome_placar.find(class_='points').get_text() for nome_placar in items]
# passa para outra parte pegando nome e indicador que depois precisa fazer a separação
items01 = soup.find_all(class_='move_action_content_text')
acao_pessoa02 = [nome_acao_pessoa02.find("p", class_='').get_text() for nome_acao_pessoa02 in items01]

dados = pd.DataFrame(
    {'Quarto': quarto,
     'Tempo': tempo,
     'Time_01': time_site,
     'Placar': placar,
     'Inf_2': acao_pessoa02
     })
