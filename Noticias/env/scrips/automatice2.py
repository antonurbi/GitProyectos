import subprocess
import re
import os
#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
#yt-dlp --write-auto-sub --skip-download --sub-format vtt --sub-lang es "url"
def descargar_subtitulos(url_video):
    # Obtener el título del video usando yt-dlp
    comando_titulo = [
        "yt-dlp",
        "--get-title",
        "--skip-download",
        f"{url_video}"
    ]
    resultado = subprocess.run(comando_titulo, check=True, capture_output=True, text=True)
    titulo_video = resultado.stdout.strip()

    # Formatear el título para usarlo como nombre de archivo
    titulo_video = re.sub(r'[^\w\s-]', '', titulo_video).replace(' ', '_')

    archivo_vtt = f"{titulo_video}.es.vtt"

    # Descargar los subtítulos
    comando_subtitulos = [
        "yt-dlp",
        "--write-auto-sub",
        "--skip-download",
        "--sub-format", "vtt",
        "--sub-lang", "es",
        "--output", archivo_vtt,
        f"{url_video}"
    ]
    subprocess.run(comando_subtitulos, check=True)

    # Encontrar el archivo .vtt descargado
    archivo_vtt_encontrado = encontrar_archivo_vtt(titulo_video)
    if archivo_vtt_encontrado:
        return titulo_video, archivo_vtt_encontrado
    else:
        return titulo_video, None




def limpiar_subtitulos(archivo_vtt):
    texto_limpio = ""
    lineas_agregadas = set()  # Conjunto para almacenar líneas únicas

    with open(archivo_vtt, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        for line in lines:
            # Ignorar líneas con marcas de tiempo o vacías
            if '-->' in line or line.strip() == '':
                continue
            
            # Limpiar etiquetas HTML/XML
            line_clean = re.sub(r'<[^>]+>', '', line).strip()

            # Agregar la línea con un salto de línea si no ha sido agregada antes
            if line_clean not in lineas_agregadas:
                texto_limpio += line_clean + "\n"
                lineas_agregadas.add(line_clean)

    return texto_limpio


def encontrar_archivo_vtt(video_id):
    print(f"Buscando archivos para el video ID: {video_id}")
    for archivo in os.listdir('.'):
        print(f"Archivo encontrado: {archivo}")
        if archivo.endswith('.vtt') and video_id in archivo:
            return archivo
    return None


def descargar_subtitulos_utimosvideos(enlace, carpeta):
    titulo_video, archivo_vtt = descargar_subtitulos(enlace)
    if archivo_vtt:
        texto_limpio = limpiar_subtitulos(archivo_vtt)
        archivo = f'/{titulo_video}_limpio.txt'
        path = carpeta + archivo
        
        # Saving the cleaned subtitle text
        with open(path, 'w', encoding='utf-8') as file_out:
            file_out.write(texto_limpio)

        # Remove the original .vtt file to clean up
        os.remove(archivo_vtt)
        

    return titulo_video,path

