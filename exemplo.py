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

# localizar_site = inf3.loc[inf3.inf2.str.contains('/pt/basketballworldcup/2019/game/', regex=True)]
localizar_site = inf3
print(localizar_site)

#i = [http://www.fiba.basketball]
# Btime = [i for item in Bindicador]
# ites.to_csv("tabela_1.csv", index=None)
'''
# encontrar o nome dos times
# ai da para fazer uma tabela geral
inf = soup.find_all(class_="header-scores_desktop")

inf_nome_A = inf[0].find(class_='team-A')
NomeA = inf_nome_A.find(class_='team-name').get_text()

inf_nome_B = inf[0].find(class_='team-B')
NomeB = inf_nome_B.find(class_='team-name').get_text()

inf_placar_A = inf[0].find(class_='score-A').get_text()
inf_placar_B = inf[0].find(class_='score-B').get_text()

inf_local = inf[0].find(class_='location').get_text()
inf_grupo = inf[0].find(class_='phase').get_text()

# fazer uma lista e depois um for para acrescentar a cada loop que fizer
print(NomeA)
print(NomeB)
print(inf_placar_A)
print(inf_placar_B)
print(inf_local)
print(inf_grupo)
'''
