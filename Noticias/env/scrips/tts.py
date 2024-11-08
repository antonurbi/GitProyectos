from gtts import gTTS

# Leer el contenido del archivo de texto
with open(r'env\Individuales-Descargas\2024-01-27\ZonasdeRuptura.txt', 'r',encoding='utf-8') as file:
    texto = file.read()

# Convertir el texto a voz
tts = gTTS(text=texto, lang='es')  # 'es' para español, cambia según necesites
tts.save('salidas.mp3')

print("Conversión completada. El audio se guardó como 'salida.mp3'")
