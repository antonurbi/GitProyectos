import openai
import textwrap

# Set the OpenAI API key using an environment variable
openai_api_key = ('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')

# Check if the API key is set
if not openai_api_key:
    raise EnvironmentError("OpenAI API key is not set in the environment variables")

openai.api_key = openai_api_key

def summarize_with_openai(text):
    # Summarize the given text using OpenAI's GPT model.
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Correct model name
            messages=[
                {"role": "system", "content": "Este es un sistema diseñado para proporcionar resúmenes y análisis en el ámbito de finanzas y tecnología."},
                {"role": "user", "content": text},
            ]
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error using OpenAI API: {e}"


def format_summary_for_readability(summary, width=80):
    # Format the summary text to enhance readability.
    return '\n'.join(textwrap.wrap(summary, width=width))

def process_ideas(file_path):
    # Process a file containing ideas by extracting key phrases and summarizing them.
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            ideas_text = file.read()

        summary = summarize_with_openai(ideas_text)
        formatted_summary = format_summary_for_readability(summary)
        return  formatted_summary
    except Exception as e:
        return [], f"Error processing ideas file: {e}"

def save_summary(summary, output_path):
    # Save the summary to a file and return the status.
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(summary)
        return f"Summary successfully saved to {output_path}"
    except Exception as e:
        return f"Error writing summary to file: {e}"

def main():
    # Generalized file paths
    ideas_file_path = 'BTC_por_debajo_de_38000_pierden_dinero_15124-9h_30m_limpio.txt'
    summary_output_path = 'resumen.txt'

    summary_text = process_ideas(ideas_file_path)
    save_status = save_summary(summary_text, summary_output_path)
    print(save_status)

main()
