from openai import OpenAI
import os

# Inicializar el cliente OpenAI con tu clave API
client = OpenAI(
    api_key="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"
)

# Función para leer el contenido de un archivo de texto
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Ruta del archivo de texto
text_file_path = 'Beli_iPhone_SE_2020_di_Tahun_2024_Masih_worth_it_gak_sih__limpio.txt'

# Leer el contenido del archivo
file_content = read_text_file(text_file_path)

# Enviar el contenido del archivo a OpenAI para su análisis
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Este es un sistema diseñado para proporcionar resúmenes y análisis sobre textos, basándose en diálogos de videos aleatorios."
        },
        {
            "role": "user",
            "content": file_content,
        },
        {
            "role": "user",
            "content": "Por favor, genera un resumen breve de este texto."
        }
    ],
    model="gpt-3.5-turbo",
    max_tokens=500,
    
)

respuesta= chat_completion.choices[0].message.content.strip()

resumen_formateado = "Resumen Breve:\n" + respuesta + "\n"

# Solicitar respuestas a las preguntas detalladas
chat_completion_preguntas = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Este es un sistema diseñado para proporcionar análisis detallados sobre textos."
        },
        {
                    "role": "user",
        "content": file_content,
        },
        {
            "role": "user",
            "content": "Considerando un texto que detalla diversas tendencias y desarrollos clave en el ámbito financiero y tecnológico, ¿cuáles son los puntos más críticos y relevantes mencionados en el texto que podrían influir significativamente en la toma de decisiones de inversión y gestión de cartera? Además, ¿cómo puedo aplicar efectivamente esta información para optimizar mi cartera de inversiones y enriquecer mi base de conocimientos en estos sectores?"
        }
    ],
    model="gpt-3.5-turbo",
    max_tokens=500,
)

respuesta1= chat_completion_preguntas.choices[0].message.content.strip()

respuesta_formateada = "Resumen Breve:\n" + respuesta1 + "\n"

# Ruta del archivo donde se guardará la respuesta
archivo_salida = 'respuesta_formateada.txt'

# Guardar la respuesta en un archivo de texto
with open(archivo_salida, 'w', encoding='utf-8') as archivo:
    archivo.write(resumen_formateado)
    archivo.write(respuesta_formateada)

print(f"Respuesta guardada en {archivo_salida}")
