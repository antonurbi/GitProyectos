from busquedacanal2 import busqueda
from proces import procesar
from rank2 import ranking
from generadorlinks import generadorlinks_ultimovideo_canal
from automatice2 import descargar_subtitulos_utimosvideos
from analyzer2 import analizar_texto

def Procesar_para_la_listacanales():
    carpeta,carpeta_salidas,api_key = busqueda() # ---> env\prueba\2024-01-19  API
    procesar(carpeta) # ---> env\EconFinan\descripcion_canales.csv
    lista_canales=ranking(carpeta) # ---> env\EconFinan\2024-01-19\lista_canales.csv
    return carpeta,lista_canales,carpeta_salidas,api_key

def ultimos_videos_canales(lista_canales,api_key):
    enlaces = generadorlinks_ultimovideo_canal(lista_canales,api_key) #yt
    enlaces = enlaces[0:3] # 0 porque hay un replace, sino se epodria saltar el encabezado con 1
    return enlaces

def analizar_transcripciones(pregunta,enlaces,carpeta,carpeta_salidas):
    for i in range(len(enlaces)):
        titulo_video = descargar_subtitulos_utimosvideos(enlaces[i][0],carpeta) #yt
        titulo_video = carpeta + f'\{titulo_video}_limpio.txt'
    analizar_texto(pregunta,titulo_video, enlaces[i][1],carpeta_salidas) # ---> env\EconFinan\2024-01-19\Salidas\Epstein.txt

    