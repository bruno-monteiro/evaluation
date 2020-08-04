# -*- coding: utf-8 -*-

import json
from random import randint
import sys
import re

import pandas as pd
import zipfile


# Aux function to order a tuple's list by the second item
def getKey(item):
    return item[1]


# Open the news file and return a random news
def open_news_file():
    news_list = []
    with open('evaluation/data/data.jsonl', 'r') as file_news:
        for line in file_news:
            news_list.append(json.loads(line))
        file_news.close()

    n = [1, 2, 3]

    index = randint(0, len(news_list) - 1)

    return news_list[index]


# Open a zip file and read the appropriate excel file result
# Return the valids toponyms form the news
def get_result_data(news_dict):
    # Extract the correct url (filename) from news
    url = news_dict['url']
    url = url.strip()
    point = url.rfind('.')
    slash = url.rfind('/')
    url = url[slash+1:point]

    # Open de zipfile
    zf = zipfile.ZipFile('evaluation/data/results_geonames.zip') 
    excel_file = '{}.xlsx'.format(url)

    teste = 'semana-nacional-do-transito-tem-programacao-educativa-em-governador-valadares.xlsx'

    tp_list =  pd.read_excel(zf.open(excel_file))['Global'].values.tolist()
    all_news = news_dict['titulo'] + news_dict['subtitulo'] + news_dict['texto']

    tp_index = []
    for toponym in tp_list:
        for index in [m.start() for m in re.finditer(toponym, all_news)]:
            tp_index.append((toponym, index, index + len(toponym) - 1))

    # Order tp_index by the index
    tp_index = sorted(tp_index, key=getKey)

    final_tps = tp_index.copy()

    # Filter the valid toponyms
    for tupla1 in final_tps:
        for tupla2 in tp_index:
            # Se os topônimos forem diferentes
            if tupla1[0] != tupla2[0]:
                # Se o topônimo for parte de outro topônimo
                if tupla1[0] in tupla2[0]:
                    # Se estiver exatamente dentro dos mesmos índices
                    if (tupla1[1] > tupla2[1]) and (tupla1[1] < tupla2[2]):
                        final_tps.remove(tupla1)

    return final_tps


# Creating toponyms buttons in news and to evaluation board
def create_buttons(news, tp_list):
    text = news['titulo'] + "||" + news['subtitulo'] + "||" + news['texto']
    index = 1
    tps = []
    for toponym in tp_list:
        span = "<sup><span class='badge badge-dark' style='font-size:10px;'>{}</span></sup>".format(index)
        html_button = "<button class='myButton' disabled>{}</button>{}".format(toponym[0].upper(), span)
        text = text.replace(toponym[0], html_button, 1)
        side_buton = "<button class='myButtonSM' disabled>{}</button>{}".format(toponym[0].title(), span)
        tps.append(side_buton)
        index += 1

    for toponym in tp_list:
        text = text.replace(toponym[0].upper(), toponym[0].title())
    
    aux_list = []
    for item in tp_list:
        aux_list.append((item[0]))

    tplist = list(zip(aux_list, tps))
    
    print(tplist, len(tplist))

    #tplist = list(zip(aux_list, tps))

    # Retun the news with buttons and a list of tp_buttons
    return (text, tplist)