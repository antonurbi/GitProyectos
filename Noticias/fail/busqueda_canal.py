from googleapiclient.discovery import build
import pandas as pd
from carpetascreator import carpetas




def youtube_service(api_key):
    
    return build('youtube', 'v3', developerKey=api_key)


def search_channels(service, query, max_results=50):
    response = service.search().list(
        q=query, #tematica
        part='snippet',
        type='channel',
        maxResults=max_results
    ).execute()
    
    return response


# Obtiene detalles adicionales de los canales, como el número de suscriptores.
def get_channel_details(service, channel_ids):
    details = service.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids)
    ).execute()
    
    return details


# Procesar los resultados de la búsqueda para extraer información relevante.
def process_results(results, service):
    channels = []
    channel_ids = [item['id']['channelId'] for item in results['items']]
    details = get_channel_details(service, channel_ids)

    for item in details['items']:
        channels.append({
            'title': item['snippet']['title'],
            'channel_id': item['id'],
            'description': item['snippet']['description'],
            'subscriber_count': item['statistics']['subscriberCount'],
            'view_count': item['statistics']['viewCount']
        })

    return pd.DataFrame(channels)


def eleccion():
    print(
        "Menu de opciones: \n"
        "1. Economía y Finanzas \n"
        "2. Infromática y Tecnología \n"
        "3. Salud Mental y Bienestar \n"
    )
    eleccion = int(input("Elige una opción: "))
    if eleccion == 1:
        query = "Economía y Finanzas"
        iniciales = "EconFinan"
    elif eleccion == 2:
        query = "Infromática y Tecnología"
        iniciales = "InfoTecn"
    elif eleccion == 3:
        query = "Salud Mental y Bienestar"
        iniciales = "SaudBien"
    else:
        print("Elige una opción válida")
        eleccion()
        
    return query, iniciales

# Realiza la búsqueda de canales, guarda los resultados en un archivo CSV y devuelve la ruta del archivo y las iniciales.
def busqueda():
    api_key = ('AIzaSyDtBOPwZ0Sks3rMtujceBebNgcY_6haWYs') #('AIzaSyAKaor6QAbB1JITNf06VJ-44s_vvrHzYXE') 
    service = youtube_service(api_key)
    
    query, iniciales = eleccion()
    
    search_results = search_channels(service, query)
    channels_df = process_results(search_results, service) #definicion de los canales 
    
    
    archivo=f'\canales.csv'
    carpeta, carpeta_salidas =carpetas(iniciales) # carpeta ---> env\EcoFinan\2024-01-19
    path=carpeta + archivo
    
    with open(path, 'w',encoding='utf-8') as f: # path ---> env\EconFinan\2024-01-19\canales.csv
        f.write(channels_df.to_csv(index=False))
    carpeta=carpeta[0:24]
    return carpeta,carpeta_salidas,api_key
  
