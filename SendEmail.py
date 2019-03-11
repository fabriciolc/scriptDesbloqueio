import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

__sender_email = "dados@inspiracao.adm.br"
__receiver_email = "moura@inspiracao.adm.br"
__server_smtp = "smtp.inspiracao.adm.br"
__port_smtp = 587
__password = "fdc00003"



def sendemail(subj,bdy,diretorio,filename):
    subject = subj
    body = bdy
    sender_email = __sender_email
    receiver_email = __receiver_email
    server_smtp = __server_smtp
    port_smtp = __port_smtp
    password = __password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    # Open file in binary mode
    with open(diretorio+filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    server = smtplib.SMTP(server_smtp,port_smtp)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

def sendFirtList(diretorio,filename):
    subject = "Lista da Semana de documentos em aberto"
    body = "Lista gerada com todas documentos aberto de 3 a 30 dias"
    sendemail(subject,body,diretorio,filename)
def sendConsPag(diretorio,filename):
    subject = "Lista de Pagamento"
    body = "Lista gerada de consultoras, que efetuou pagamento"
    sendemail(subject,body,diretorio,filename)
def sendListFinal(diretorio,filename):
    subject = "Lista final"
    body = "Lista final dos documentos que ainda estão em aberto"
    sendemail(subject,body,diretorio,filename)
