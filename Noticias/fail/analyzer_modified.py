from openai import OpenAI
from datetime import datetime

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
            {"role": "user", "content": "Por favor, genera un resumen breve de este texto."}
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
def formatear_texto(titulo, contenido):
    palabras = contenido.split()
    contenido_formateado = "\n".join([" ".join(palabras[i:i+18]) for i in range(0, len(palabras), 10)])
    return f"{titulo}\n{'=' * len(titulo)}\n{contenido_formateado}\n\n"

def guardar_respuestas_en_archivo(resumen, respuesta_detallada, nombre_canal):
    resumen_formateado = formatear_texto("Resumen Breve", resumen)
    respuesta_detallada_formateada = formatear_texto("Respuesta Detallada", respuesta_detallada)

    # Combina todo en un solo texto
    texto_final = resumen_formateado + respuesta_detallada_formateada
    data = datetime.now()
    time=data.strftime('%d/%m/%Y %M:%S')
    name=f'{nombre_canal}{time}'
    name=name.replace(' ','').replace(',','').replace(':','').replace('/','').replace('@','')
    with open(f'{name}.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(texto_final)

    print(f"Texto formateado guardado en 'texto_formateado.txt'.")


def analizar_texto(titulo_video, nombre_canal):
    api_key = "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"
    client = inicializar_cliente_openai(api_key)
    pregunta_detallada = "Considerando un texto que detalla diversas tendencias y desarrollos clave en el ámbito financiero y tecnológico, ¿cuáles son los puntos más críticos y relevantes mencionados en el texto que podrían influir significativamente en la toma de decisiones de inversión y gestión de cartera? Además, ¿cómo puedo aplicar efectivamente esta información para optimizar mi cartera de inversiones y enriquecer mi base de conocimientos en estos sectores?"
    file_content = leer_archivo_texto(titulo_video)
    resumen = obtener_resumen_openai(client, file_content)
    respuesta_detallada = obtener_respuestas_detalladas_openai(client, file_content, pregunta_detallada)
    guardar_respuestas_en_archivo(resumen, respuesta_detallada, nombre_canal)




# Función para eliminar repeticiones en un texto.
 


def procesar_texto(file_path):
    texto = leer_archivo_texto(file_path)
    texto_sin_repetir = eliminar_repeticiones(texto)
    return obtener_resumen_openai(client, texto_sin_repetir)
