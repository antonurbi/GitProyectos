# Full script including a main function to automate the process of summarizing a text file containing ideas

import os
import openai
import nltk
from textblob import TextBlob
import textwrap

# Configuration: API Key and NLTK setup
# Load OpenAI API key from an environment variable for security
openai_api_key = ('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')

# Set the OpenAI API key if it's available
if openai_api_key:
    openai.api_key = openai_api_key

# Download the NLTK brown dataset if not already downloaded
nltk.download('brown', quiet=True)

def extract_key_phrases(text, num_phrases=10):
    """
    Extract key phrases from the given text using TextBlob.

    Args:
    text (str): The input text from which to extract key phrases.
    num_phrases (int): Number of key phrases to extract.

    Returns:
    str: A string containing the extracted key phrases.
    """
    blob = TextBlob(text)
    key_phrases = blob.noun_phrases[:num_phrases]
    return ' '.join(key_phrases)

def summarize_with_openai(text):
    """
    Summarize the given text using OpenAI's GPT model.

    Args:
    text (str): The text to be summarized.

    Returns:
    str: The summarized text or an error message.
    """
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-1106",  # Correct model name
            messages=[
                {"role": "system", "content": "Este es un sistema diseñado para proporcionar información y análisis en el ámbito de finanzas y tecnología, basándose en diálogos de videos aleatorios."},
                {"role": "user", "content": "¿Cómo se pueden aplicar las tendencias actuales en tecnología financiera para innovar en la creación y gestión de proyectos financieros?"},
            ]
        )




        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error using OpenAI API: {e}"

def format_summary_for_readability(summary, width=80):
    """
    Format the summary text to enhance readability by wrapping the text.

    Args:
    summary (str): The summary text to be formatted.
    width (int): The maximum line width for the formatted text.

    Returns:
    str: The formatted summary text.
    """
    return '\n'.join(textwrap.wrap(summary, width=width))

def process_ideas(file_path):
    """
    Process a file containing ideas by extracting key phrases and summarizing them.

    Args:
    file_path (str): Path to the file containing ideas.

    Returns:
    str: The summarized text or an error message.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            ideas_text = file.read()

        key_phrases = extract_key_phrases(ideas_text)
        summary = summarize_with_openai(key_phrases)
        formatted_summary = format_summary_for_readability(summary)
        return formatted_summary
    except Exception as e:
        return f"Error processing ideas file: {e}"

def save_summary(summary, output_path):
    """
    Save the summary to a file.

    Args:
    summary (str): The summary text to be saved.
    output_path (str): Path to the output file where the summary will be saved.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"Summary successfully saved to {output_path}")
    except Exception as e:
        print(f"Error writing summary to file: {e}")

def main():
    
    """
    Main function to run the process of summarizing ideas.
    """
    # Example file paths (update these paths with your actual file paths)
    ideas_file_path = 'BALAS_MACHETES_Y_ROBOS_-_LA_VIDA_EN_BOGOTÁ_limpio.txt'
    summary_output_path = 'resumen.txt'

    summary_text = process_ideas(ideas_file_path)
    save_summary(summary_text, summary_output_path)

# Uncomment the following line to run the script
main()
