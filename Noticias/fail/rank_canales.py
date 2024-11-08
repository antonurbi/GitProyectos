import pandas as pd
from carpetascreator import carpetas
def load_data(file_path):
    """
    Carga los datos de canales de YouTube desde un archivo CSV.
    """
    return pd.read_csv(file_path)

def transform_data(data):
    """
    Transforma los datos para incluir enlaces completos y mantener las columnas especificadas.
    """
    # Convertir channel_id en un enlace de YouTube
    data['link_canal'] = data['channel_id'].apply(lambda x: f'https://www.youtube.com/channel/{x}')

    # Mantener las columnas especificadas y agregar la columna de enlace
    columns = ['title', 'link_canal', 'subscriber_count', 'view_count', 'normalized_views']
    data = data[columns]
    data.sort_values(by='view_count', ascending=False, inplace=True)
    return data

def save_to_csv(data, output_file):
    """
    Guarda el DataFrame modificado en un nuevo archivo CSV.
    """
    data.to_csv(output_file, index=False)

def ranking(carpeta):
    archivo='\descripcion_canales.csv'
    input_file_path = carpeta + archivo # ---> env\EconFinan\2024-01-19\descripcion_canales.csv
    output_file_path = carpeta + '\lista_canales.csv' # menu 

    # Cargar los datos
    channels_data = load_data(input_file_path)

    # Transformar los datos
    processed_data = transform_data(channels_data)

    # Guardar en un nuevo archivo CSV
    save_to_csv(processed_data, output_file_path)

    print(f"Datos procesados guardados en: {output_file_path}")
    return output_file_path

