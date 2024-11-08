import os
import speech_recognition as sr
from pytube import YouTube
from pydub import AudioSegment
from pocketsphinx import AudioFile, get_model_path
from pydub.effects import normalize

def preprocesar_audio(audio_file):
    try:
        # Carga el archivo de audio
        audio = AudioSegment.from_file(audio_file)

        # Normaliza el volumen
        audio = normalize(audio)

        # Aquí podrías añadir más procesamiento si es necesario

        # Guarda el archivo procesado
        audio.export(audio_file, format="wav")

    except Exception as e:
        print(f"Error al procesar el audio: {e}")

def youtube_audio_descargador(link):
    try:
        yt = YouTube(link)
        # Intenta encontrar un flujo de audio en formato WAV directamente
        audio_stream = yt.streams.filter(only_audio=True, file_extension='webm').first()
        if not audio_stream:
            # Si no hay un flujo en formato WAV, descarga el mejor flujo de audio disponible
            audio_stream = yt.streams.filter(only_audio=True).first()
        
        print('Descargando audio...')
        output_file = audio_stream.download()

        if not os.path.exists(output_file):
            print('El audio no se ha descargado correctamente.')
            return False

        # Convierte el archivo descargado a formato WAV si no está en ese formato
        if not output_file.endswith('.wav'):
            audio = AudioSegment.from_file(output_file)
            wav_file = f"{os.path.splitext(output_file)[0]}.wav"
            audio.export(wav_file, format="wav")
            os.remove(output_file)  # Elimina el archivo original si es necesario
            output_file = wav_file
        preprocesar_audio(output_file)
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return False

    
def transcribir_audio(audio_file):
    model_path = get_model_path()

    configuracion_audio = AudioFile(
        verbose=False,
        audio_file=os.path.abspath(audio_file),
        hmm=os.path.join(model_path, 'Es-es\es-es'),
        lm=os.path.join(model_path, 'Es-es\es-20k.lm.bin'),
        dic=os.path.join(model_path, 'Es-es\cmudict-es-es.dict')
    )

    transcripcion = []
    for frase in configuracion_audio:
        transcripcion.append(str(frase))

    transcripcion_completa = ' '.join(transcripcion)
    print(transcripcion_completa)
    return transcripcion_completa


def main():
    link = input('Ingrese el link del video: ')
    mp3_archivo = youtube_audio_descargador(link)

    if mp3_archivo:
        transcripcion_mp3 = transcribir_audio(mp3_archivo)
        print(transcripcion_mp3)  # Imprimir la transcripción

if __name__ == '__main__':
    main()


# salida: WARN: "ngram_search.c", line 391: Word 'acto' survived for 5374 frames, potential overpruning
# WARN: "ngram_search.c", line 391: Word 'acto' survived for 5374 frames, potential overpruning
# en acto en un acto
# en acto en un acto