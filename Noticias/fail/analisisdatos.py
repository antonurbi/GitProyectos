import pandas as pd

def load_data(file_path):
    """
    Carga los datos de canales de YouTube desde un archivo CSV.
    """
    return pd.read_csv(file_path)

def rank_channels(data, peso_suscriptores=0.5, peso_vistas=0.5):
    """
    Clasifica los canales basado en una puntuación compuesta de suscriptores y vistas normalizadas.
    """
    data['composite_score'] = (
        peso_suscriptores * data['normalized_subscribers'] + 
        peso_vistas * data['normalized_views']
    )
    ranked_data = data.sort_values(by='composite_score', ascending=False)
    return ranked_data

def main():
    input_file_path = 'processed_channels.csv'
    output_file_path = 'ranked_channels.csv' # rank 

    # Cargar los datos
    channels_data = load_data(input_file_path)

    # Clasificar los canales y guardar en un nuevo archivo CSV
    ranked_channels = rank_channels(channels_data)
    ranked_channels.to_csv(output_file_path, index=False)

    print(f"Canales clasificados guardados en: {output_file_path}")

if __name__ == "__main__":
    main()
