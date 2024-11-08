from openai import OpenAI
from preanalyzer import preanalyzer



def inicializar_cliente_openai(api_key):
    return OpenAI(api_key=api_key)

def leer_archivo_texto(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def obtener_resumen_openai(client, file_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Este es un sistema diseñado para proporcionar resúmenes y análisis sobre textos, basándose en diálogos de videos aleatorios."},
            {"role": "user", "content": file_content},
            {"role": "user", "content": "Por favor, genera un resumen breve de los datos a destacar de esta transcripcion."}
        ],
        model="gpt-3.5-turbo",
        max_tokens=500
    )
    return chat_completion.choices[0].message.content.strip()

def obtener_respuestas_detalladas_openai(client, file_content, pregunta):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Este es un sistema diseñado para proporcionar análisis detallados sobre textos."},
            {"role": "user", "content": file_content},
            {"role": "user", "content": pregunta}
        ],
        model="gpt-3.5-turbo",
        max_tokens=500
    )
    return chat_completion.choices[0].message.content.strip()

def funcion_formatear_texto(titulo,contenido):
    palabras = contenido.split()
    contenido_formateado = []
    contador = 0
    nueva_linea = True
    contenido_formateado.append('\n\n' + titulo + "\n\n")
    for palabra in palabras:
        if nueva_linea:
            contenido_formateado.append(palabra)
            nueva_linea = False
        else:
            contenido_formateado.append(" " + palabra)
        contador += 1

        # nueva linea despues de 20 palabras o despues de un punto o dos puntos
        if contador == 20 or palabra.endswith('.') or palabra.endswith(':'):
            contenido_formateado.append("\n")
            contador = 0
            nueva_linea = True

    return "".join(contenido_formateado)

def formatear_texto(resumen,respuesta_detallada): # Junta el resumen y la respuesta detallada en un solo texto
    resumen_formateado = funcion_formatear_texto('RESUMEN',resumen)
    respuesta_formateada = funcion_formatear_texto('CONTENIDO',respuesta_detallada)
    texto_final =  resumen_formateado + respuesta_formateada
    return texto_final 


def guardar_respuestas_en_archivo(texto_final, nombre_canal, carpeta_salidas):

    name = nombre_canal.replace(' ','').replace(',','').replace(':','').replace('/','').replace('@','') # ---> Salidas/fecha/nombre_canal.txt
    file_name = f'\{name}.txt'
    path=  carpeta_salidas + file_name
    with open(path, 'w', encoding='utf-8') as archivo: # ---> env\EconFinan\2024-01-19\Salidas\Epstein.txt
        archivo.write(texto_final)
    print(f"Texto formateado guardado en {path}.")


def analizar_texto(pregunta,titulo_video, nombre_canal,carpeta_salidas):
    api_key = "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"
    client = inicializar_cliente_openai(api_key)
    transcrip = leer_archivo_texto(titulo_video)
    resumen,sep = preanalyzer(transcrip)
    # Limita la lista de resúmenes al número actual disponible (sep)
    resumenes_a_procesar = resumen[:sep]
    texto_final_total = ""
    for file_content in resumenes_a_procesar:
        resumen = obtener_resumen_openai(client, file_content)
        respuesta_detallada = obtener_respuestas_detalladas_openai(client, file_content, pregunta)
        texto_final = formatear_texto(resumen, respuesta_detallada)
        texto_final_total += texto_final
    guardar_respuestas_en_archivo(texto_final_total, nombre_canal,carpeta_salidas)

def analizar_texto2(titulo_video, nombre_canal,carpeta_salidas):
    api_key = "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"
    client = inicializar_cliente_openai(api_key)
    transcrip = leer_archivo_texto(titulo_video)
    resumen,sep = preanalyzer(transcrip)
    # Limita la lista de resúmenes al número actual disponible (sep)
    resumenes_a_procesar = resumen[:sep]
    for file_content in resumenes_a_procesar:
        resumen = obtener_resumen_openai(client, file_content)
        texto_final = funcion_formatear_texto('RESUMEN',resumen)
    guardar_respuestas_en_archivo(texto_final, nombre_canal,carpeta_salidas)