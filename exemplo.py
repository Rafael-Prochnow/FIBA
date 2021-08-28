from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


r = requests.get('http://www.fiba.basketball/en/basketballworldcup/2019/games')
soup = BeautifulSoup(r.content, 'html.parser')
inf = soup.find_all(class_="latest_qualifier_games")

inf2 = [a['href'] for a in soup.find_all('a', href=True)]
inf3 = pd.DataFrame({'inf2': inf2})

tamano = len(inf3)
NomeA = str('http://www.fiba.basketball/en')
Atime = [NomeA for item in range(0, tamano)]
inf3['inf4'] = Atime

inf3['nomedanovacoluna'] = inf3.inf4.str.cat(inf3.inf2)
inf3.drop('inf4', axis=1, inplace=True)
inf3.drop('inf2', axis=1, inplace=True)

p2_site = inf3.loc[inf3.nomedanovacoluna.str.contains('http://www.fiba.basketball/en/basketballworldcup/2019/game/',
                                                      regex=True)]

########################################################################################################################
# lista = p2_site.values.tolist()
# lista.translate[remove_punctuation(i) for i in train_pos]
# print(lista)

colunas = ['coluna1', 'coluna2', 'coluna3']
tabela_geral = pd.DataFrame(index=['0', '1', '2', '3', '4'])

for i in p2_site.nomedanovacoluna.values:
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

    nome_coluna = [NomeA + NomeB]
    tabela_geral[nome_coluna] = pd.DataFrame(informacoes, index=tabela_geral.index)
    print(tabela_geral)

    # encontrar o nome dos times
    # ai da para fazer uma tabela geral
    inf = soup_site.find_all(class_="header-scores_desktop")
    infA = inf[0].find(class_='team-A')
    NomeA = infA.find(class_='team-name').get_text()
    infB = inf[0].find(class_='team-B')
    NomeB = infB.find(class_='team-name').get_text()

    ####################################################################################################################
    jogada_jogada = soup_site.find(class_="selected-periods")
    # enocntrar o primiero time
    # por que estou separando por time?
    # cada ação (jogada a jogada) o site não registra o time, mas sim a orgem visual no site, e no codigo está por
    # <li class="action-item x--team-A"> ai como não consigo pegar essa informação eu estou separando os times e o inici
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
    ####################################################################################################################
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

    # Lance livres

    a = saparar.apply(lambda x: re.sub('(2nd of 2 free throws made|1st of 2 free throws made|'
                                       '1st free throw made|1st of 2 free throw made|'
                                       '3rd of 3 free throws made|2nd of 3 free throws made|'
                                       '1st of 3 free throws made|)', '9/LL_Pts_C', x))
    a = a.apply(lambda x: re.sub('(1st of 2 free throws missed|2nd of 2 free throws missed|'
                                 '1st free throw missed|1/ 3 free throws awarded)', '9/LL_Pts_T', x))

    # dois pontos

    a = a.apply(lambda x: re.sub('(2pt pullup jump shot made|2pt fadeaway jump shot made|'
                                 '2pt jump shot from center made|2pt floating jump shot made|'
                                 '2pt driving layup made|Arremesso de dois certo|Bandeja Certa|'
                                 '2pt driving layup made|2pt hook shot made|2pt putback dunk made|'
                                 '2pt turnaround jump shot made|2pt Arr. Certo)', '9/2_Pts_C', x))

    a = a.apply(lambda x: re.sub('(2pt pullup jump shot missed|2pt fadeaway jump shot missed|'
                                 '2pt jump shot from center blocked|2pt jump shot from center missed|'
                                 '2pt floating jump shot blocked|2pt floating jump shot missed|'
                                 '2pt driving layup missed|Arremesso de dois errado|Bandeja Errada|'
                                 '2pt driving layup blocked|2pt driving layup missed|2pt hook shot missed|'
                                 '2pt putback dunk missed|2pt jump shot blocked|2pt turnaround jump shot missed|'
                                 '2pt Arr. Errado|Tip In Errada|layup blocked)', '9/2_Pts_T', x))

    a = a.apply(lambda x: re.sub('(Arremesso de tres certo|3pt jump shot from center made|'
                                 '3pt pullup jump shot made|3pt step back jump shot made|'
                                 '3pt turnaround jump shot made|Tip In Certa)', '9/3_Pts_C', x))

    a = a.apply(lambda x: re.sub('(Arremesso de tres errado|3pt jump shot from center missed|'
                                 '3pt pullup jump shot missed|3pt step back jump shot missed|'
                                 '3pt turnaround jump shot missed)', '9/3_Pts_T', x))

    # rebotes
    a = a.str.replace('defensive rebound', '9/RD')
    a = a.str.replace('offensive rebound', '9/RO')
    # recuperação de bola
    a = a.str.replace('steal', '9/BR')
    # assistencias
    a = a.str.replace('made the assist', '9/AS')
    # palarvras aleatórias
    a = a.apply(lambda x: re.sub('( 2 free throws awarded| 1 free throw awarded|team |'
                                 ' 3 free throws awarded| 5 seconds violation|24 seconds violation|'
                                 '1st of 1 )', '', x))
    # 5 Faltas
    a = a.str.replace('unsportsmanlike foul 2 free throws awarded', '9/FC_A')
    a = a.str.replace('personal foul', '9/FC')
    a = a.str.replace('offensive foul', '9/FC_O')
    a = a.str.replace('technical foul', '9/FC_T')
    a = a.str.replace('foul drawn', '9/FR')
    # substituição
    a = a.str.replace('Substitution in', '9/substituicao_entra')
    a = a.str.replace('Substitution out', '9/substituicao_sai')
    # erros
    a = a.apply(lambda x: re.sub('(turnover ball handling|turnover travelling|turnover bad pass|'
                                 'turnover 3 seconds violation|turnover out of bounds)', '9/ER', x))

    # tocos
    a = a.str.replace('blocked the shot', '9/TO')
    # tempo técnico
    a = a.str.replace('Timeout', '9/tempo_tecnico')
    # cravada
    a = a.str.replace('Enterrada', '9/EN')
    # ponte aerea
    a = a.str.replace('Ponte Aerea Errada', '9/EN_T')
    a = a.str.replace('Ponte Aerea Certa', '9/EN')
    # bola no alto
    a = a.str.replace('jump ball won', '9/inicio_quarto')
    a = a.str.replace('jump ball situation throw-in', '9/muda_bola')
    # não sei
    a75 = a74.str.replace('', '9/2_Pts_T')
    a76 = a75.str.replace('', '9/2_Pts_C')
    a78 = a77.str.replace('', '9/2_Pts_T')
    a79 = a78.str.replace('free throw made', '9/LL_Pts_T')
    a80 = a79.str.replace('turnover', '9/ER')
    a81 = a80.str.replace('2pt step back jump shot made', '9/2_Pts_C')
    a82 = a81.str.replace('2pt step back jump shot missed', '9/2_Pts_T')
    a83 = a82.str.replace('2pt step back jump shot blocked', '9/2_Pts_T')
    a84 = a83.str.replace('2pt jump shot inside the paint missed', '9/2_Pts_T')
    a85 = a84.str.replace('2pt jump shot inside the paint made', '9/2_Pts_C')
    a86 = a85.str.replace('', '')

    a87 = a86.str.replace('2nd of 3 free throws missed', '9/LL_Pts_T')
    a88 = a87.str.replace('3nd of 3 free throws missed', '9/LL_Pts_T')
    a89 = a88.str.replace('1nd of 3 free throws missed', '9/LL_Pts_T')
    a90 = a89.str.replace('3rd of 3 free throws missed', '9/LL_Pts_T')
    a91 = a90.str.replace('1st of 3 free throws missed', '9/LL_Pts_T')
    a92 = a91.str.replace('', '')
    a93 = a92.str.replace('', '')
    a94 = a93.str.replace('2pt hook shot blocked', '9/2_Pts_T')
    a95 = a94.str.replace('', '')
    a96 = a95.str.replace('3pt jump shot from center blocked', '9/3_Pts_T')

    # nome;1/indicador
    # estou fazendo isso pq tem indicadores que não tem jogadores(noomes)
    # quando coloco 1 ele ajuda a separa os dois e deixar uma variável 1 quando não tem nome
    # depois eu tiro esse ;1 e coloco um identificador do time
    mudados_00 = a96.str.split('/')
    mudados_01 = mudados_00.str.get(1)
    dados['Indicador'] = mudados_01

    mudados_02 = mudados_00.str.get(0)
    mudados_03 = mudados_02.str.replace('9', '')
    mudados_04 = mudados_03.str.replace(';', '')
    dados['Nome'] = mudados_04

    dados.drop('Inf_2', axis=1, inplace=True)
    dados.to_csv("tabela_1.csv", index=None)
    dados.to_csv("./Dados03/tabela_FIBA_" + NomeA + "_" + NomeB + ".csv", index=None)

tabela_Final = tabela_geral.T
print(tabela_Final)
