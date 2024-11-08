import os
from pytube import YouTube
link = "https://www.youtube.com/watch?v=xuAqQcQV2hI"
yt= YouTube(link)
print(yt) 
print(yt.title) #titulo del video
print(yt.thumbnail_url) #url de la imagen
print(yt.length) #duracion del video
print(yt.author) #autor del video
print(yt.views) #numero de vistas
print(yt.streams) #calidad de video

#obtener la mayor resolucion
ys = yt.streams.get_highest_resolution()

ys = yt.streams.get_by_itag('22') #obtener el video en 720p
print('descargando...')
ys.download() #descargar el video

#extraer el audio del video
ys = yt.streams.filter(only_audio=True).first()
print('descargar audio...')
out_file = ys.download() #archivo de audio
print('audio descargado...')

basename = os.path.basename(out_file) #nombre del archivo
print(basename)
nombre, formato = os.path.split('.') #separar el nombre del archivo de la extension

audio_file = f'{nombre}.mp3' #nombre del archivo de audio
print(audio_file)