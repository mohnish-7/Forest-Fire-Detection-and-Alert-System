import cv2
import time
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from os import system
import smtplib
from email.message import EmailMessage
import imghdr

# Global variables

model = load_model('../Models/ffd_model.h5')
frc = 0
count = 0
mail_sent = False

# ---------------------------------------------------------- Function to Clear the screen --------------------------------------------------- #
def clear():
    system('cls')

    
    
# ---------------------------------------------------------- Function to Save an image ------------------------------------------------------ #    
def save_img(img,fname):
    
    dir = r'../Email_Content'
    os.chdir(dir)
    
    try:
        cv2.imwrite(fname,img)
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Img Captured XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        time.sleep(1.5)
        return True
    
    except:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Something Went Wrong while saving the image XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        raise   
        return False

        
        
# ------------------------------------------------------- Function to send a mail ----------------------------------------------------------- #

def send_mail(n):
    
    email_address = 'forestfiredetection16@gmail.com'
    password = 'forestfire'

    msg = EmailMessage()
    msg['Subject'] = 'FOREST FIRE ALERT !'
    msg['From'] = email_address
    msg['To'] = email_address
    msg.set_content('A FIRE has been detected at a forest area near you. Stay Safe !')

    files = ['Local_Fire_Capture_1','Local_Fire_Capture_2','Local_Fire_Capture_3']

    for file in files[:n]:
        with open('../Email_Content/'+file+'.jpg','rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name

        msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name[17:])


    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        try:
            smtp.login(email_address,password)
            smtp.send_message(msg)
            return True
            
        except:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Something Went Wrong, while sending the email XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            return False

        
        
# ------------------------------------------------------ Function to make a Prediction ------------------------------------------------------ #
    
def predict(img):
    
    clear()
    
    img = image.img_to_array(img)
    img = np.expand_dims(img,axis=0)
    img = img / 255
    
    confidence = model.predict(img)
    
    res = (confidence[0][0] > 0.80).astype(np.int32)
    if res == 0:        
        return True,confidence
        
    else:
        return False,confidence
        

        
###############################################################################################################################################
#                                                                 Main 
###############################################################################################################################################

cap = cv2.VideoCapture('../Video_Test_Data/Fire/Fire_4.mp4')
fps = int(cap.get(cv2.CAP_PROP_FPS)) 

while True and cap.isOpened():
    
    
    ret,frame = cap.read()
    
    if ret == True:
        
        img = frame
        mail_img = img
        img = cv2.resize(img,(250,250))
        
        fire,confidence = predict(img)
        
        if fire:
            
            print('FIRE DETECTED !'+'\nWith confidence score: {:.3f} '.format((1-confidence[0][0])*100))
            frc += 1
            if frc % 75 == 0 and count < 3:
                
                fname = 'Local_Fire_Capture_'+str(count+1)+'.jpg'
                
                if save_img(mail_img,fname):
                    count += 1
                
                if count == 3:
                    mail_sent = send_mail(count)
                    
                    
                    
        else:
            print('No Fire Detected.'+'\nWith confidence score: {:.3f} '.format((confidence[0][0])*100))
                    
            
        
        frame = cv2.resize(frame,(900,600))
        #time.sleep(1/fps)
        cv2.imshow('Video Feed',frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    else:
        break
        
cap.release()        
cv2.destroyAllWindows()

if not mail_sent and count > 0:
    #print('\n',count,'\n')
    send_mail(count)
    mail_sent = True

if mail_sent:
    print('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n       MAIL SENT SUCCESSFULLY       \n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

