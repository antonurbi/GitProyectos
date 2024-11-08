# Import necessary libraries
import imaplib
import email
import yaml  # To load saved login credentials from a yaml file
from datetime import datetime, timedelta
from datetime import datetime
from email.header import decode_header
import webbrowser
import os


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)
def data():
    data = datetime.now()
    time=data.strftime('%Y/%m/%d')
    print(time)
    return time.replace(' ','-').replace(',','').replace(':','').replace('/','-').replace('@','')
def carpeta_salidas2(iniciales):
    base_path = r"C:\Proyectos\gmailscript"
    date=data()
    # Base directory set to env
    folder_path = os.path.join(base_path, iniciales, date)  # Path for the new folder within env

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    full_file_path = os.path.join(folder_path)
    return full_file_path
def get_emails(emaill):
    # Load credentials from YAML file
    with open("credentials.yml") as f:
        content = f.read()
    my_credentials = yaml.load(content, Loader=yaml.FullLoader)
    # Assign the username and password from the yaml file
    user, password = my_credentials["user"], my_credentials["password"]
    # URL for IMAP connection
    imap_url = 'imap.gmail.com'
    # Connect to Gmail via SSL
    my_mail = imaplib.IMAP4_SSL(imap_url)
    # Log in to the mailbox
    my_mail.login(user, password)
    # Select the Inbox to fetch messages
    my_mail.select('Inbox')
    # Define a date range (last 3 days)
    date_n_days_ago = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
    # Define search filters
    # We will use 'SINCE' for the last 3 days and 'FROM' to filter by sender
    key = 'SINCE'
    search_criteria = f'(SINCE {date_n_days_ago} FROM "{emaill}")'
    # Search for emails based on the criteria
    _, data = my_mail.search(None, search_criteria)
    # Get the list of email IDs
    mail_id_list = data[0].split()
    return my_mail,mail_id_list
def get_msgs(my_mail,mail_id_list, salida):
    # Initialize an empty list to capture the messages
    msgs = []
    news_items = []
    s=0
    # Iterate through the list of mail IDs and fetch each message
    for num in mail_id_list:
        typ, data = my_mail.fetch(num, '(RFC822)')  # Fetch the entire message
        msgs.append(data)
    # Now, process and display the fetched emails
    for msg in msgs[::-1]:
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    try:
                    # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    except:
                        subject = subject.decode('utf-8')
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                # print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print("Subject:", clean(subject) + " \n" + "-"*40)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                folder_name= salida + "\\" + folder_name
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        #print(body)
                        print("Subject:", clean(subject) + " \n" + "-"*40)
                        

                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    folder_name = clean(subject)
                    folder_name =salida + "\\" + folder_name
                    if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                        os.mkdir(folder_name)
                    filename = "index.html"
                    filepath = os.path.join(folder_name, filename)
                    # write the file
                    open(filepath, "w",encoding='UTF-8').write(body)
                    
                    print(rf"Link to the news: file:///{filepath.replace('\ ','/')}")
    # close the connection and logout
    my_mail.close()
    my_mail.logout()
def main_1():
    print("""
      LISTA DE NOTICIAS:
        1. TLDR
        2. MANSION GLOBAL
        3. Seeking Alpha
        4. The Daily Upside
        5. Morning Brew
        6. Crypto Briefing
        7. Brew Markets
        8. Cointelegraph 
        9. Bloomberg
      """)
    num = int(input("Ingrese el número de la noticia que desea leer: "))
    if num == 1:
        nombre = "TLDR"
        emaill = "dan@tldrnewsletter.com"
    elif num == 2:
        nombre = "MANSION_GLOBAL"
        emaill = "MansionGlobal@t.dowjones.com"
    elif num == 3:
        nombre= "Seeking_Alpha"
        emaill= "account@seekingalpha.com"
    elif num == 4:
        nombre= "The_Daily_Upside"
        emaill= "squad@thedailyupside.com"
    elif num == 5:
        nombre= "Morning_Brew"
        emaill= "andrew@bearbulltraders.com"
    elif num == 6:
        nombre= "Crypto_Briefing"
        emaill= "editor@cryptobriefing.com"
    elif num == 7:
        nombre= "Brew_Markets"
        emaill= "crew@morningbrew.com"
    elif num == 8:
        nombre= "Cointelegraph"
        emaill= "OneMinuteLetter@cointelegraph.com"
    elif num == 9:
        nombre= "Bloomberg"
        emaill= "noreply@news.bloomberg.com"
    salida=carpeta_salidas2(nombre)
    my_mail,mail_id_list=get_emails(emaill)
    get_msgs(my_mail,mail_id_list, salida)

def main_2():
    email_dict = {
        1: {"nombre": "TLDR", "emaill": "dan@tldrnewsletter.com"},
        2: {"nombre": "MANSION_GLOBAL", "emaill": "MansionGlobal@t.dowjones.com"},
        3: {"nombre": "Seeking_Alpha", "emaill": "account@seekingalpha.com"},
        4: {"nombre": "The_Daily_Upside", "emaill": "squad@thedailyupside.com"},
        5: {"nombre": "Morning_Brew", "emaill": "andrew@bearbulltraders.com"},
        6: {"nombre": "Crypto_Briefing", "emaill": "editor@cryptobriefing.com"},
        7: {"nombre": "Brew_Markets", "emaill": "crew@morningbrew.com"},
        8: {"nombre": "Cointelegraph", "emaill": "OneMinuteLetter@cointelegraph.com"},
        9: {"nombre": "Bloomberg", "emaill": "noreply@news.bloomberg.com"}
    }
    for i in range(1,10):
        salida = carpeta_salidas2(email_dict[i]["nombre"])
        my_mail,mail_id_list=get_emails(email_dict[i]["emaill"])
        get_msgs(my_mail,mail_id_list, salida)
        
if __name__ == "__main__":
    print("""
        1. main_1 (selección)
        2. main_2 (completo)
            """)
    num = int(input("Numero: "))
    if num == 1:
        main_1()
    elif num == 2:
        main_2()
    
    
    
    """
    login 87232667
    contraseña !c4hEoSj
    inverso SiJ!0pBq  (Contraseña de solo lectura)
    """