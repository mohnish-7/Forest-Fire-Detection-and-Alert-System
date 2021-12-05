import smtplib
from email.message import EmailMessage
import imghdr

email_address = 'forestfiredetection16@gmail.com'
password = 'forestfire'

msg = EmailMessage()
msg['Subject'] = 'FOREST FIRE ALERT !'
msg['From'] = email_address
msg['To'] = email_address
msg.set_content('A FIRE has been detected at a forest area near you. Stay Safe !')

files = ['Local_Fire_Capture_1','Local_Fire_Capture_2','Local_Fire_Capture_3']

for file in files:
    with open('../Email_Content/'+file+'.jpg','rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name[17:])


with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    
    smtp.login(email_address,password)
    smtp.send_message(msg)