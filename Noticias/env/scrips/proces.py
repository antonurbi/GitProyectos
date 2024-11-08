# Correcting the path issue and ensuring the 'normalized_subscribers' column is created and accessed correctly
import pandas as pd
import matplotlib.pyplot as plt
from carpetascreator import carpetas

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

# Improving the 'generate_report' function for a more attractive and functional chart


def generate_report(data):
    # Automate report generation and visualization
    plt.figure(figsize=(12, 8))
    
    # Creating the bar plot
    bars = plt.bar(data['title'], data['normalized_subscribers'], color='skyblue')

    # Adding a title and labels
    plt.xlabel('Channel Title', fontsize=14)
    plt.ylabel('Normalized Subscriber Count', fontsize=14)
    plt.title('YouTube Channel Subscriber Analysis', fontsize=16)

    # Improving the legibility of x-ticks
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Annotating the bar with the highest subscriber count
    max_subscriber = data['normalized_subscribers'].max()
    for bar in bars:
        if bar.get_height() == max_subscriber:
            plt.annotate(f'Max: {max_subscriber:.2f}', 
                         (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                         ha='center', va='bottom', fontsize=12, color='green')

    plt.tight_layout()
    plt.show()



def save_to_csv(data, output_file):
    data.to_csv(output_file, index=False)

def procesar(carpeta):
    archivo = r'\canales.csv'
    input_file_path = carpeta + archivo
    output_file_path = carpeta + r'\descripcion_canales.csv'

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



