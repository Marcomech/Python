import requests
from bs4 import BeautifulSoup
import webbrowser


BaseUrl = 'https://tpb.party/'

def search_torrents(BaseUrl):
    Titulo = input('Titulo: ').replace(' ', '%20') 
    URL = BaseUrl + 'search/' + Titulo+ '/1/99/200'
    page = requests.get(URL)
    #print(page.text)
    return page

def get_movies(BaseUrl):
    page = search_torrents(BaseUrl)
    soup = BeautifulSoup(page.content, "html.parser")

    resultados = soup.find(id = "searchResult")

    peliculas1 = resultados.find_all("tr", class_="alt")
    peliculas2 = resultados.find_all("tr", class_="")
    peliculas  = []

    for i in range(0,5):
        peliculas.append(peliculas1[i])
        peliculas.append(peliculas2[i])

    return(peliculas)


peliculas = get_movies(BaseUrl)   
d = {}
for pelicula in peliculas:
    titulo = pelicula.find("div", class_="detName")

    links = pelicula.find_all("a")
    #print(titulo.text.strip())
    for link in links:
        link_url = link["href"]
        if link_url.startswith('magnet:'):
            d[titulo.text.strip()] = link_url
            #print(link_url)

for key in d:
    print(key)
    if (input('Descargas (y/n):') == 'y'):
        webbrowser.open(d[key])
        break