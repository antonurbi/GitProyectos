from menu import *
from carpetascreator import *
from analyzer2 import *
from busquedacanal2 import *
from automatice2 import descargar_subtitulos_utimosvideos


def escribir_menu():
    print("Resumenes videos de Youtube")
    print("-------------------")
    print("")
    print("1. Resumen canales, por tematica")
    print("2. Descargar resumen de un video de Youtube")
    print("3. Descargar resumen de un video con pregunta personalizada")
    print("4. Descargar 1 video")
    print("5. Descargar Links")

def menu():
    VALOR_MIN = 1
    VALOR_MAX = 5

    opcion_valida = False
    while not opcion_valida:
        escribir_menu()

        try:
            opcion = int(
                input("Seleccione una opcion entre %d y %d: \n" % (VALOR_MIN, VALOR_MAX))
            )
            if opcion >= VALOR_MIN and opcion <= VALOR_MAX:
                opcion_valida = True
        except ValueError:
            opcion_valida = False

        if not opcion_valida:
            print(
                "Error. Opcion invalida, introduzca un numero entre %d y %d."
                % (VALOR_MIN, VALOR_MAX)
            )

    return opcion

def pregunta_detallada():
    pregunta = '''
    Me gustaría obtener un análisis completo de la transcripccion de un video . ¿Podrías proporcionar un resumen detallado que incluya los siguientes aspectos?
    1. **Tema Principal y Objetivos:** ¿Cuál es el tema central y los objetivos del video?
    2. **Estructura y Secciones Clave:** ¿Cómo está organizado el video y qué se trata en cada sección?
    3. **Personajes o Presentadores:** ¿Quiénes son los principales personajes o presentadores y cuál es su importancia?
    4. **Datos o Estadísticas Importantes:** ¿Se mencionan datos, estadísticas o estudios relevantes?
    5. **Argumentos o Puntos Clave:** ¿Cuáles son los argumentos o puntos principales?
    6. **Ejemplos o Casos de Estudio:** ¿Se usan ejemplos o casos de estudio específicos?
    7. **Gráficos, Imágenes o Elementos Visuales:** ¿Qué tipo de elementos visuales se usan y cómo contribuyen al mensaje?
    8. **Conclusiones o Llamados a la Acción:** ¿Cuáles son las conclusiones o los llamados a la acción?
    9. **Referencias Externas:** ¿Hay referencias a fuentes externas, libros o artículos?
    10. **Comentarios o Interacciones Significativas:** Si es aplicable, ¿hay comentarios o interacciones del público que sean relevantes?"
    '''
    return pregunta

def main():
    salir = False
    while not salir:
        opcion = menu()
        
        if opcion == 1:
            carpeta,lista_canales,carpeta_salidas,api_key = Procesar_para_la_listacanales()
            enlaces = ultimos_videos_canales(lista_canales,api_key)
            for i in range(len(enlaces)):
                titulo_video = descargar_subtitulos_utimosvideos(enlaces[i][0],carpeta) #yt
                titulo_video = carpeta + f'\{titulo_video}_limpio.txt'
                analizar_texto2(titulo_video, enlaces[i][1],carpeta_salidas) # ---> env\EconFinan\2024-01-19\Salidas\Epstein.txt

        elif opcion == 2:
            salida=carpeta_salidas2('Individuales-Descargas')
            enlaces = []
            print('Introduce el link de esta manera: https://www.youtube.com/watch?v=zmedQfBQwuQ')
            url_video = input('Link: ')
            nombre_video = input('Nombre del video: ')
            enlaces.append([url_video,nombre_video])
            promt = pregunta_detallada()
            analizar_transcripciones(promt,enlaces,salida,salida)
            
        elif opcion == 3:
            salida=carpeta_salidas2('Individuales-Personalizadas')
            enlaces = []
            print('Introduce el link de esta manera: https://www.youtube.com/watch?v=zmedQfBQwuQ')
            url_video = input('Link: ')
            nombre_video = input('Nombre del video: ')
            pregunta = input('Pregunta: ')
            enlaces.append([url_video,nombre_video])
            for i in range(len(enlaces)):
                titulo_video = descargar_subtitulos_utimosvideos(enlaces[i][0],salida) #yt
                titulo_video = salida + f'\{titulo_video}_limpio.txt'
                analizar_texto(pregunta,titulo_video,nombre_video,salida)
        
        elif opcion == 4:
            salida=carpeta_salidas2('Individuales-Personalizadas')
            print('Introduce el link de esta manera: https://www.youtube.com/watch?v=zmedQfBQwuQ')
            url_video = input('Link: ')
            titulo_video,path = descargar_subtitulos_utimosvideos(url_video,salida) #yt

        elif opcion == 5:
            link3 = "https://www.youtube.com/watch?v=-JngOjEkPk8"
            links = [link3]
            for link in links:
                salida=carpeta_salidas2('Individuales-Personalizadas')
                titulo_video,path = descargar_subtitulos_utimosvideos(link,salida) #yt
        
            
        elif opcion == 6:
            salir = True

        if not salir:
            print("Pulsa Intro para continuar")
            


if __name__ == "__main__":
    main()
    
