import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException
import urllib
import re


dados = pd.read_csv('tabela_1.csv')
saparar = dados["Inf_2"]
a = ['personal foul']
dados = dados[0]
# separar nome e indicador
# lance livre

'''
for c in saparar:
    if saparar.str.contains('personal foul'):
        saparar.replace(c, '9/FC')
        print(saparar)
saparar(dados)

str.contains
if ft made
elif ft missed
elif 2pt made
elif 2pt missed
'''
