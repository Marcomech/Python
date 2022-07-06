import requests
from bs4 import BeautifulSoup
import webbrowser

BaseUrl = "https://yifysubtitles.org/movie-imdb/"

def magnet(Hash, Movie):
    torrent = "magnet:?xt=urn:btih:"+\
    Hash+"&dn="+Movie+\
    "&tr=udp://tracker.cyberia.is:6969"+\
    "/announce&tr=udp://tracker.port443.xyz:6969"+\
    "/announce&tr=http://tracker3.itzmx.com:6961"+\
    "/announce&tr=udp://tracker.moeking.me:6969"+\
    "/announce&tr=http://vps02.net.orel.ru:80"+\
    "/announce&tr=http://tracker.openzim.org:80"+\
    "/announce&tr=udp://tracker.skynetcloud.tk:6969"+\
    "/announce&tr=https://1.tracker.eu.org:443"+\
    "/announce&tr=https://3.tracker.eu.org:443"+\
    "/announce&tr=http://re-tracker.uz:80"+\
    "/announce&tr=https://tracker.parrotsec.org:443"+\
    "/announce&tr=udp://explodie.org:6969"+\
    "/announce&tr=udp://tracker.filemail.com:6969"+\
    "/announce&tr=udp://tracker.nyaa.uk:6969"+\
    "/announce&tr=udp://retracker.netbynet.ru:2710"+\
    "/announce&tr=http://tracker.gbitt.info:80"+\
    "/announce&tr=http://tracker2.dler.org:80/announce"
    return torrent
    

def chose(rango):
    nro = -10
    while 1 > nro or rango < nro:
        try:
            nro = int(input("Elija un numero: "))
        except ValueError:
            print ("No fue un numero")
    return nro

def get_list_movies():
        Titulo = input('Titulo: ').replace(' ', '-') 
        uri = 'https://yts.torrentbay.to/api/v2/list_movies.json?sort_by=download_count&query_term='+ Titulo
        json = requests.get(uri).json()

        movie_count = json['data']['movie_count']
        while movie_count < 1:
            print('No hay peliculas llamadas: ', Titulo)
            Titulo = input('Titulo: ').replace(' ', '-') 
            uri = 'https://yts.torrentbay.to/api/v2/list_movies.json?sort_by=download_count&query_term='+ Titulo
            json = requests.get(uri).json()
            movie_count = json['data']['movie_count']

        list_movies = json['data']['movies']
        return list_movies

def select_movie():
    movie_list = get_list_movies()
    print("\n******************************************")
    print(  "*************    Pelicula    *************")
    print(  "******************************************")
    i=0
    for movie in movie_list:
        i=i+1
        print("\n\nOpcion",i)
        print(movie['title_long'])
    
    nro = chose(i)

    return movie_list[nro-1]

def select_quality(movie):
    print("\n******************************************")
    print(  "*************    Calidad     *************")
    print(  "******************************************")
    print("\n (se recomienda 720p o 1080p)")

    i=0
    for torrent in movie['torrents']:
        i=i+1
        print("\n\nOpcion",i)
        print('\nCalidad: '+ torrent['quality'])

    eleccion = chose(i)

    return movie['torrents'][eleccion-1]['hash']

###########Subtitulos###########
def get_list(BaseUrl, Titulo):

    page = requests.get(BaseUrl + Titulo)
    soup = BeautifulSoup(page.content, "html.parser")


    table     = soup.find("table", class_="table other-subs")
    body      = table.find("tbody", class_="")
    element   = body.find_all("tr")

    options = []
    for i in element:
        lang = i.find("td", class_="flag-cell")
        option = []
        if lang.text == 'Spanish':
            
            score = i.find("td", class_="rating-cell").text
            download = i.find("a")
            link = 'https://yifysubtitles.org/' +download.get('href').replace('subtitles', 'subtitle')+'.zip'
            description = download.text
            option.append(score) 
            option.append(description.split("\n")[0])
            option.append(link)

            options.append(option)

    if (input("Desea subtitulos (y/n): ") == "n"):
        options =[]
    return options


def select_subtitulo(BaseUrl, Titulo):
    options = get_list(BaseUrl, Titulo)
    if (options == []):
        print("No hay subtitulos disponibles")
        return False, False
    print("\n******************************************")
    print(  "*************   Subtitulos   *************")
    print(  "******************************************")
    for i in range(0, len(options)):
        print("\nOpcion", i+1)
        print("Titulo: "+options[i][1] ," ------->Puntaje: "+options[i][0])

    subtitulo = options[int(input('Elija una opcion para los subtitulos: '))-1][2]

    return True, subtitulo



Movie = select_movie()
print(Movie['title_long'])

torrent = magnet(select_quality(Movie), Movie['title_long'])

Id = Movie['imdb_code']

(status, subtitulo) = select_subtitulo(BaseUrl, Id)
if status:
    webbrowser.open(subtitulo)
webbrowser.open(torrent)









