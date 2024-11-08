from googleapiclient.discovery import build
from urllib.parse import urlparse   # parse_qs : para obtener el id del video 
                                    # urlparse : para obtener el nombre del canal



def leer_canales(archivo_canales):
    with open(archivo_canales, 'r',encoding='utf-8') as archivo:
        return [linea.strip().split(',')[0:2] for linea in archivo.readlines()[1:]]


def buscar_canal_por_nombre(api_key, canal_id):
    # Inicializar el cliente de la API de YouTube
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Realizar la solicitud para obtener detalles del canal
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=canal_id
    )
    response = request.execute()

    # Verificar si se obtuvieron resultados
    if 'items' in response and response['items']:
        # Aquí podrías extraer más detalles si lo necesitas
        return response['items'][0]
    else:
        return None


def obtener_ultimo_video(api_key, enlace_canal):
    # Extraer el ID del canal del enlace
    parsed_url = urlparse(enlace_canal)
    canal_id = parsed_url.path.split('/')[-1]

    # Obtener detalles del canal usando el ID
    detalles_canal = buscar_canal_por_nombre(api_key, canal_id)

    if detalles_canal:
        youtube = build('youtube', 'v3', developerKey=api_key)
        # Último video
        request = youtube.search().list(
            part="snippet",
            channelId=canal_id,
            maxResults=1,
            order="date"
        )
        response = request.execute()

        if 'items' in response and response['items']:
            ultimo_video_id = response['items'][0]['id'].get('videoId',None)
        if ultimo_video_id is not None:
            enlace_ultimo_video = f"https://www.youtube.com/watch?v={ultimo_video_id}"
            return enlace_ultimo_video, detalles_canal['snippet']['title']
        else:
            # Handle the case where no videoId is found
            return None, None


    
    
def generadorlinks_ultimovideo_canal(archivo_canales,api_key):
    enlaces=[]
    enlaces_canales = leer_canales(archivo_canales)
    for i in range(len(enlaces_canales)):
        enlace_ultimo_video = obtener_ultimo_video(api_key, enlaces_canales[i][1])
        enlaces.append(enlace_ultimo_video)
    return enlaces


