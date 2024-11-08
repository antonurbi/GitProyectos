import spacy

# Cargando el modelo en español de spaCy
nlp = spacy.load('es_core_news_sm')

def formatear_texto(titulo, contenido):
    # Dividir el contenido en oraciones
    doc = nlp(contenido)
    oraciones = [sent.text.strip() for sent in doc.sents]

    # Eliminar repeticiones
    oraciones_unicas = []
    for oracion in oraciones:
        if oracion not in oraciones_unicas:
            oraciones_unicas.append(oracion)

    # Unir las oraciones únicas en bloques de texto
    contenido_formateado = "\n\n".join([" ".join(oraciones_unicas[i:i+3]) for i in range(0, len(oraciones_unicas), 3)])

    return f"{titulo}\n{'=' * len(titulo)}\n{contenido_formateado}\n\n"

# Aplicar la función formateada al contenido del archivo
titulo = "Resumen Modificado"
with open('InvierteConEdu160120245005.txt', 'r', encoding='utf-8') as archivo:
    content = archivo.read()
print(content)
contenido_formateado = formatear_texto(titulo, content)

# Mostrar los primeros 1000 caracteres del contenido formateado
print(contenido_formateado)
