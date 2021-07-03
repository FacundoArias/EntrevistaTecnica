import json

def buscarPelis(genero,tipo):
    arrAux = []
    for elem in data[tipo]:
        if genero in elem['generos']:
            arrAux.append({
                "titulo": elem["titulo"],
                "url": elem["url"]
            })
    return arrAux

with open('datos.json') as file:
    data = json.load(file)

    print(f' cantidad peliculas: {len(data["peliculas"])}')
    print(f' cantidad series: {len(data["series"])}')

    #BUSCO PELICULAS POR GENERO PARA UN USUARIO DEVUELVO URL Y NOMBRE DE LA PELICULA
    tipo = input('ingrese (peliculas) si deseas buscar peliculas o ingrese (series) si deseas buscar series: ')
    genero = input('Ingrese genero de pelicula que deseas buscar: ')
    arr_peliculas = buscarPelis(genero, tipo)
    print (f'Las {tipo} encontradas para el genero {genero} son las siguientes : ')
    for elem in arr_peliculas:
        print(elem)