# Correcting the path issue and ensuring the 'normalized_subscribers' column is created and accessed correctly

import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_and_normalize(data):
    # Fill missing values in descriptions
    data['description'].fillna('Sin descripción', inplace=True)
    # Normalize 'subscriber_count' and 'view_count'
    data['normalized_subscribers'] = data['subscriber_count'] / data['subscriber_count'].max()
    data['normalized_views'] = data['view_count'] / data['view_count'].max()
    return data

def analyze_data(data):
    # Adding more in-depth analysis of the data
    # Placeholder for additional analysis
    pass

def generate_report(data):
    # Automate report generation and visualization
    plt.figure(figsize=(10, 6))
    plt.bar(data['title'], data['normalized_subscribers'])
    plt.xlabel('Channel Title')
    plt.ylabel('Normalized Subscriber Count')
    plt.title('YouTube Channel Subscriber Analysis')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def save_to_csv(data, output_file):
    data.to_csv(output_file, index=False)

def procesar(carpeta):
    archivo = r'\canales.csv'
    input_file_path = carpeta 
    output_file_path = carpeta + r'\prueba_canales.csv'

    # Load and process the data
    channels_data = load_data(input_file_path)
    processed_data = clean_and_normalize(channels_data)

    # Additional data analysis
    analyze_data(processed_data)

    # Generate reports and visualizations
    generate_report(processed_data)

    # Save the processed data to a new CSV file
    save_to_csv(processed_data, output_file_path)
    print(f"Datos procesados guardados en: {output_file_path}")

# Example usage
if __name__ == "__main__":
    carpeta = r'env\InfoTecn\2024-01-21\lista_canales.csv'
    procesar(carpeta)

