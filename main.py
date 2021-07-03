from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

def guardarDatosEnJson():
    with open('datos.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, )

def cerrarVentana():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def scrollPagina():
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def nuevaVentanaGenero(elem):
    driver.find_element_by_id('navItens').click()
    elem.send_keys(Keys.CONTROL + Keys.RETURN)
    driver.switch_to.window(driver.window_handles[1])


def setUrl(url):
    #Este set es dejar acomodado la url ya que no la extraigo directamente de un src
    #si no que la saco del atributo 'onClick' que ejecuta el metodo de navegar a esa pagina
    nuevaUrl = ''
    bool = False

    for elem in url:

        if elem == ')':
            bool = False

        if bool:
            nuevaUrl += elem

        if elem == '(':
            bool = True

    return nuevaUrl.replace("'", "")


def getLinksPeliculas():
    contenedor_peliculas = driver.find_element_by_class_name('detach')
    peliculas = contenedor_peliculas.find_elements_by_tag_name('li')

    for pelicula in peliculas:
        img = pelicula.find_element_by_tag_name('img')
        link_peli = setUrl(img.get_attribute('onclick'))
        url_peliculas.add(link_peli)

def extraerInformacion():
    contenedor_titulo_distribuidora = driver.find_element_by_class_name('detailsTitleContainer')
    titulo = contenedor_titulo_distribuidora.find_element_by_class_name('detailTitle').text
    distribuidora = contenedor_titulo_distribuidora.find_element_by_class_name('detailDistributor').text
    contenedor_duracion_anio_lugar = driver.find_element_by_class_name('ageContainer')
    arr_contenedor_duracion_anio_lugar = (
        contenedor_duracion_anio_lugar.find_element_by_class_name('detailsYear').text).split('|')
    anio = arr_contenedor_duracion_anio_lugar[0]
    lugar = arr_contenedor_duracion_anio_lugar[1]
    duracion = arr_contenedor_duracion_anio_lugar[2]
    contenedor_generos_pelicula = (driver.find_element_by_class_name('detailsGenre').text).split(',')
    descripcion = driver.find_element_by_class_name('detailsSynopsi').text
    contenedor_protagonitas_directores = driver.find_elements_by_class_name('movieActorsContainer')
    contenedor_protagonistas = contenedor_protagonitas_directores[0].find_elements_by_tag_name('a')
    contenedor_directores = contenedor_protagonitas_directores[1].find_elements_by_tag_name('a')
    arr_protagonistas = []
    arr_directores = []
    url_actual = driver.current_url

    for protagonista in contenedor_protagonistas:
        arr_protagonistas.append(protagonista.get_attribute('innerHTML'))

    for director in contenedor_directores:
        arr_directores.append(director.get_attribute('innerHTML'))

    try:
        contenedor_capitulos = driver.find_element_by_class_name('movieEpisodes')
        arr_capitulos = contenedor_capitulos.find_elements_by_class_name('episodeContainer')
        data_capitulos = {'capitulos': []}

        for capitulo in arr_capitulos:
            data_capitulos['capitulos'].append({
                'titulo': capitulo.find_element_by_class_name("episodeName").text,
                'descripcion': (capitulo.find_element_by_class_name("episodeSynopsis").text).replace(
                    f'{capitulo.find_element_by_class_name("episodeName").text}\n', ""),
                'duracion': capitulo.find_element_by_tag_name("span").text
            })

        data['series'].append({
            'titulo': titulo,
            'distribuidora': distribuidora,
            'anio': anio,
            'lugar': lugar,
            'duracion': duracion,
            'descripcion': descripcion,
            'generos': contenedor_generos_pelicula,
            'protagonistas': arr_protagonistas,
            'director': arr_directores,
            'url': url_actual,
            'capitulos': data_capitulos['capitulos']
        })
    except:
        data['peliculas'].append({
            'titulo': titulo,
            'distribuidora': distribuidora,
            'anio': anio,
            'lugar': lugar,
            'duracion': duracion,
            'descripcion': descripcion,
            'generos': contenedor_generos_pelicula,
            'protagonistas': arr_protagonistas,
            'director': arr_directores,
            'url': url_actual
        })

def recorrerPeliculasYExtraerInformacion(peliculas):
    for pelicula in peliculas:
        try:
            driver.get(f'https://www.looke.com.br{pelicula}')
            extraerInformacion()
        except:
            pass

def obtenerGeneros():
    link_generos_temp = []
    contenedor_generos = driver.find_elements_by_class_name('menuItem')
    for elem in contenedor_generos:
        generos = elem.find_elements_by_class_name('headerMenuItenDescription')
        for genero in generos:
            link_generos_temp.append(genero)
    return link_generos_temp

def obtenerUrlPeliculas(generos):
    #Aca lo que hago es abrir genero en otra ventana
    #Hay 2 generos que no cargan entonces creo un try
    #catch para que no se me rompa el programa y simplemente
    #cierre la ventana que tire eror y siga
    for elem in generos:
        try:
            nuevaVentanaGenero(elem)
            time.sleep(3)
            scrollPagina()
            getLinksPeliculas()
            cerrarVentana()
        except:
            cerrarVentana()
            pass

if __name__ == '__main__':
    #Declaro la ruta que voy a buscar y la abro
    url = "https://www.looke.com.br/home"
    path = 'C:\chromedriver'
    driver = webdriver.Chrome(path)
    driver.get(url)

    data = {'peliculas': [], 'series': []}

    #Recorro la barra de navegacion para obtener los generos
    link_generos = obtenerGeneros()

    #Creo un set de arr peliculas para posteriormente guardar las urls y que no se repitan
    url_peliculas = set()
    #Recorro genero por genero para extraer las urls
    obtenerUrlPeliculas(link_generos)

    #Recorro todos los links extraidos y comienzo a guardar la informacion en un json
    recorrerPeliculasYExtraerInformacion(url_peliculas)

    #Cierro la pagina
    driver.close()

    #Guardo los datos en formato json
    guardarDatosEnJson()


