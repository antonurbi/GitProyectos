def numero_de_tokens(texto):
    average_characters_per_token = 4
    estimated_tokens = len(texto) / average_characters_per_token
    print(f"Tokens estimados: {estimated_tokens:,.0f}")
    
    return estimated_tokens

def dividir(texto,sep):
    if sep == 2:
        resumen1 = texto[0:2000]
        resumen2 = texto[2000:4000]
        return resumen1,resumen2
        
    elif sep == 3:
        resumen1 = texto[0:2000]
        resumen2 = texto[2000:4000]
        resumen3 = texto[4000:6000]
        return resumen1,resumen2,resumen3
        
    elif sep == 4:
        resumen1 = texto[0:2000]
        resumen2 = texto[2000:4000]
        resumen3 = texto[4000:6000]
        resumen4 = texto[6000:8000]
        return resumen1,resumen2,resumen3,resumen4
        

def decision(estimated_tokens,num):
    if estimated_tokens < num:
        return True
    else:
        return False
    
    
def preanalyzer(text_content):
    estimated_tokens = numero_de_tokens(text_content)
    if decision(estimated_tokens,2000):
        return text_content,1
    
    elif decision(estimated_tokens,4000):
        resumen1,resumen2 = dividir(text_content,2)
        resumen=[resumen1,resumen2]
        return resumen,2
    
    elif decision(estimated_tokens,6000):
        resumen1,resumen2,resumen3 = dividir(text_content,3)
        resumen=[resumen1,resumen2,resumen3]
        return resumen,3
    
    elif decision(estimated_tokens,8000):
        resumen1,resumen2,resumen3,resumen4 = dividir(text_content,4)
        resumen=[resumen1,resumen2,resumen3,resumen4]  
        return resumen,4
    else:
        print('No se puede dividir el texto en mas de 4 partes')
        resumen1,resumen2,resumen3,resumen4 = dividir(text_content,4)
        resumen=[resumen1,resumen2,resumen3,resumen4]
        return resumen,4
    