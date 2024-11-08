def leer_canales():
    with open('canales.csv', 'r') as archivo:
        return [linea.strip().split(',')[:2] for linea in archivo.readlines()[1:]]
    
def buscar_canal_por_nombre():
    canales=leer_canales()
    print(canales)
    enlaces=[]
    for i in range(len(canales)):
        enlaces.append(canales[i])
    print(enlaces)
    return enlaces

def main():
    enlaces=buscar_canal_por_nombre()
    print(enlaces)
    for i in range (len(enlaces)):
        print(enlaces[i][1])
        
if __name__ == '__main__':
    main()

# Crea un servicio de YouTube API utilizando la clave de API proporcionada.
def youtube_service(api_key):
    """
    Crea un servicio de YouTube API.
    """
    return build('youtube', 'v3', developerKey=api_key)

# Realiza una búsqueda de canales en YouTube basada en una consulta.
def search_channels(service, query, max_results=50):
    """
    Busca canales en YouTube basado en una consulta.
    """
    response = service.search().list(
        q=query,
        part='snippet',
        type='channel',
        maxResults=max_results
    ).execute()
    return response

# Obtiene detalles adicionales de los canales, como el número de suscriptores.
def get_channel_details(service, channel_ids):
    """
    Obtiene detalles adicionales de los canales, como número de suscriptores.
    """
    details = service.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids)
    ).execute()
    return details

# Procesa los resultados de la búsqueda para extraer información relevante.
def process_results(results, service):
    """
    Procesa los resultados de la búsqueda para extraer información relevante.
    """
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

# Muestra un menú de opciones y devuelve la consulta y las iniciales correspondientes.
def eleccion():
    print(
        "Menu de opciones: \n"
        "1. Economía y Finanzas \n"
        "2. Infromática y Tecnología \n"
        "3. Salud Mental y Bienestar \n"
    )
    eleccion = input("Elige una opción: ")
    if eleccion == "1":
        query = "Economía y Finanzas"
        iniciales = "EconFinan"
    elif eleccion == "2":
        query = "Infromática y Tecnología"
        iniciales = "InfoTecn"
    elif eleccion == "3":
        query = "Salud Mental y Bienestar"
        iniciales = "SaudBien"
    else:
        print("Elige una opción válida")
        eleccion()
    return query, iniciales

# Realiza la búsqueda de canales, guarda los resultados en un archivo CSV y devuelve la ruta del archivo y las iniciales.
def busqueda():
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    service = youtube_service(api_key)
    query, iniciales = eleccion()
    search_results = search_channels(service, query)
    channels_df = process_results(search_results, service)
    nombre = f'{iniciales}'
    archivo = f'canales{nombre}.csv'
    carpeta = carpetas(nombre, archivo)
    with open(carpeta, 'w', encoding='utf-8') as f:
        f.write(channels_df.to_csv(index=False))
    return carpeta, iniciales