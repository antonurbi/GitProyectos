from datetime import datetime
import os
def data():
    data = datetime.now()
    time=data.strftime('%Y/%m/%d')
    print(time)
    return time.replace(' ','-').replace(',','').replace(':','').replace('/','-').replace('@','')
def carpeta_salidas(iniciales):
    base_path = "env"
    date=data()
    # Base directory set to env
    folder_path = os.path.join(base_path, iniciales, date, 'Salidas')  # Path for the new folder within env

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    full_file_path = os.path.join(folder_path)
    return full_file_path

def carpetas(iniciales):
    file_salidas = carpeta_salidas(iniciales)
    base_path = "env"
    date=data()
    # Base directory set to env
    folder_path = os.path.join(base_path, iniciales, date)  # Path for the new folder within env

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    full_file_path = os.path.join(folder_path)
    return full_file_path, file_salidas

def carpeta_salidas2(iniciales):
    base_path = r"C:\Proyectos\Noticias\env"
    date=data()
    # Base directory set to env
    folder_path = os.path.join(base_path, iniciales, date)  # Path for the new folder within env

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    full_file_path = os.path.join(folder_path)
    return full_file_path