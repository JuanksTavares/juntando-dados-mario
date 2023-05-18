import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st


def pegarDadosJuan():
    progress_text = "Carregando dados, por favor aguarde."
    my_bar = st.progress(0, text=progress_text)

    progress = 1
    url = "https://imobiliariaavenida.com.br/venda/residencial/" 
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    myInfoArray = []

    links = soup.find_all('a', class_='titulo-grid')

        
    for link in links:
        pushHref = link['href']
        newResponse = requests.get(pushHref)
        newSoup = BeautifulSoup(newResponse.content, 'html.parser')
        title = newSoup.find('h1').get_text()
        value = newSoup.find('span', class_='thumb-price').get_text()
        area_before = newSoup.find('div', id='amenity-area-total')
        area = area_before
        if area != None:
            area = area.find('span').get_text()
        description = newSoup.find('p').get_text()
        
        aux = [title, value, area, description]
        myInfoArray.append(aux)

        progress_percent = (progress / len(links))
        my_bar.progress(progress_percent, text=progress_text)     
        progress += 1


    df = pd.DataFrame(myInfoArray, columns=['Título', 'Valor', 'Area','Descricao'])
    return df

#def gerarCSV():
#    df.to_excel('scrapImobiliaria.xlsx', index=False)
 #   df.to_csv('scrapImobiliaria.csv', index=False)

