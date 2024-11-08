'''
El costo es de 0.07371000000000001 por 200 lineas y 1365 palabras. 
El costo de 0.4212 por 1000 linea y 7800 palabras.

'''

# Tarifas por token de entrada y salida
precio_por_entrada_token = 0.0030  
precio_por_salida_token = 0.0060  

# Caso 1: 200 líneas - 1,365 palabras
lineas_caso_1 = 200
palabras_caso_1 = 1365
tokens_por_palabra = 15  

# Estimación de tokens de entrada y salida para el caso 1
tokens_entrada_caso_1 = palabras_caso_1 * tokens_por_palabra
tokens_salida_caso_1 = (tokens_entrada_caso_1 / 1000) * 100

# Costo estimado para el caso 1
costo_entrada_caso_1 = (tokens_entrada_caso_1 / 1000) * precio_por_entrada_token
costo_salida_caso_1 = (tokens_salida_caso_1 / 1000) * precio_por_salida_token

# Caso 2: 1,000 líneas - 7,800 palabras
lineas_caso_2 = 1000
palabras_caso_2 = 7800

# Estimación de tokens de entrada y salida para el caso 2
tokens_entrada_caso_2 = palabras_caso_2 * tokens_por_palabra
tokens_salida_caso_2 = (tokens_entrada_caso_2 / 1000) * 100

# Costo estimado para el caso 2
costo_entrada_caso_2 = (tokens_entrada_caso_2 / 1000) * precio_por_entrada_token
costo_salida_caso_2 = (tokens_salida_caso_2 / 1000) * precio_por_salida_token

print(costo_entrada_caso_1 + costo_salida_caso_1, costo_entrada_caso_2 + costo_salida_caso_2)
