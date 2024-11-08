# from urllib.parse import urlparse
# def leer_canales(archivo_canales):
#     with open(archivo_canales, 'r',encoding='utf-8') as archivo:
#         return [linea.strip().split(',')[0:2] for linea in archivo.readlines()[1:]]
    
# def obtener_ultimo_video( enlace_canal):
#     # Extraer el ID del canal del enlace
#     parsed_url = urlparse(enlace_canal)
#     canal_id = parsed_url.path.split('/')[2]
#     print(canal_id)
    
# archivo_canales = 'processed_channelsoy.csv'
# enlaces_canales = leer_canales(archivo_canales)
# obtener_ultimo_video(enlaces_canales[0][1])

def formatear_texto(contenido):
    palabras = contenido.split()
    contenido_formateado = []
    contador = 0
    nueva_linea = True

    for palabra in palabras:
        # Check for special headers and add extra line break
        if palabra in ['RESUMEN', 'CONSIDERAR']:
            contenido_formateado.append('\n' + palabra + "\n\n")
            nueva_linea = True
            continue

        if nueva_linea:
            contenido_formateado.append(palabra)
            nueva_linea = False
        else:
            contenido_formateado.append(" " + palabra)

        contador += 1

        # Add a new line after 20 words, a period, or a colon
        if contador == 20 or palabra.endswith('.') or palabra.endswith(':'):
            contenido_formateado.append("\n")
            contador = 0
            nueva_linea = True

    return "".join(contenido_formateado)


resumen='''
 El texto habla sobre la posibilidad de deducir gastos del SAT para reducir el pago de impuestos. Se menciona la importancia de pagar con medios electrónicos y tener las facturas correctas. Los beneficios se verán reflejados en la declaración de impuestos del año siguiente. También se menciona la opción de aprender más sobre inversiones.Los puntos críticos y relevantes mencionados en el texto son los siguientes:

- El SAT permite deducir ciertos gastos para pagar menos impuestos.
- Se mencionan algunas categorías de gastos deducibles.
- Se indica que es importante pagar con medio electrónico y solicitar facturas con los datos correctos.
- Los beneficios de las deducciones se verán hasta abril de 2025, si se aplicaron en el año 2024.
- Si se aplicaron en el año 2023, los beneficios se recibirán en abril del año siguiente.
'''

respuesta='''
Para aplicar esta información y optimizar tu cartera de inversiones, puedes considerar lo siguiente:

1. Evaluar los gastos deducibles mencionados en el texto y determinar si alguno de ellos se aplica a tus actividades económicas. Si es así, podrías hacer uso de estas deducciones para reducir tu carga fiscal y tener más capital para invertir.

2. Investigar más sobre las categorías de gastos deducibles que se mencionan en el texto. Esto te permitirá tener un conocimiento más detallado sobre qué tipo de gastos son considerados por el SAT y cómo puedes optimizar tus finanzas personales en función de ello.

3. Investigar otras estrategias de inversión y planificación fiscal. Comprender cómo funcionan los impuestos y las deducciones te ayudará a tomar decisiones más informadas a la hora de invertir y gestionar tu dinero.

4. Mantenerte actualizado sobre los cambios en las leyes fiscales y las regulaciones del SAT. Esto te permitirá adaptar tu estrategia de inversión y aprovechar al máximo las oportunidades y beneficios fiscales disponibles.

En resumen, aplicar la información del texto te permitirá utilizar estrategias de deducciones fiscales para optimizar tu cartera de inversiones y, al mismo tiempo, enriquecerte en conocimientos sobre el mundo de las inversiones y las regulaciones fiscales.
    '''

texto_final = 'RESUMEN ' + resumen + 'CONSIDERAR' + respuesta

resumen_formateado = formatear_texto(texto_final) #b
with open('sucui.txt', 'w', encoding='utf-8') as archivo:
    archivo.write(resumen_formateado)