# Integrating the advanced ranking system and data transformation in the 'ranking' function

import pandas as pd
import matplotlib.pyplot as plt
from carpetascreator import carpetas

def load_data(file_path):
    return pd.read_csv(file_path)

def transform_data(data):
        # Convertir channel_id en un enlace de YouTube
    data['link_canal'] = data['channel_id'].apply(lambda x: f'https://www.youtube.com/channel/{x}')

    # Mantener las columnas especificadas y agregar la columna de enlace
    columns = ['title', 'link_canal', 'subscriber_count', 'view_count', 'normalized_views']
    data = data[columns]
    data.sort_values(by='view_count', ascending=False, inplace=True)
    return data

def rank_channels(data):
    # Advanced ranking algorithm
    # Ranking based on multiple criteria like subscriber count, view count
    data['rank'] = data[['subscriber_count', 'view_count']].apply(lambda x: x['subscriber_count'] + x['view_count'], axis=1).rank(ascending=False)
    return data.sort_values(by='rank')

def visualize_ranking(data):
    # Visualizing the ranking
    plt.figure(figsize=(12, 8))
    plt.bar(data['title'][:10], data['rank'][:10])  # Visualizing top 10 channels
    plt.xlabel('Channel Title')
    plt.ylabel('Rank')
    plt.title('Top 10 YouTube Channels')
    plt.xticks(rotation=45)
    plt.show()

def save_to_csv(data, output_file):
    data.to_csv(output_file, index=False)

def ranking(carpeta):
    archivo='\descripcion_canales.csv'
    input_file_path = carpeta + archivo # ---> env\EconFinan\2024-01-19\descripcion_canales.csv
    output_file_path = carpeta + '\lista_canales.csv' # menu 
    # Load and process the data
    channels_data = load_data(input_file_path)
    processed_data = transform_data(channels_data)

    # Rank the channels
    ranked_data = rank_channels(processed_data)

    # Visualize the rankings
    visualize_ranking(ranked_data)

    # Save to CSV
    save_to_csv(ranked_data, output_file_path)

    print(f"Datos procesados guardados en: {output_file_path}")
    return output_file_path