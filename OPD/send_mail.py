from random import randint
from email.message import EmailMessage
import smtplib


def send_email_otp(to):
   try:
      otp=randint(1000,99999)
      body="OTP From e_vaccination portal\nYour OTP is: "+str(otp)
      subject="e-Vaccination"
      msg = EmailMessage()
      msg.set_content(body)
      msg['subject']=subject
      msg['to'] = to

      user = "sarveshgandhere2002@gmail.com"
      msg['from']=user
      password = "kburswetbalyszew"

      server = smtplib.SMTP("smtp.gmail.com",587)
      server.starttls()
      server.login(user,password)
      server.send_message(msg)
      server.quit()
   except:
      return "False"
   else:
      return str(otp)
   
def send_certificate_link(path,to):
   try:
      #path=path.replace(" ","%")
      body="You can download your certificate from below link\nProvide your mail id And first name and last name on: "+path
      subject="e-Vaccination Certifiacte"
      msg = EmailMessage()
      msg.set_content(body)
      msg['subject']=subject
      msg['to'] = to

      user = "sarveshgandhere2002@gmail.com"
      msg['from']=user
      password = "kburswetbalyszew"

      server = smtplib.SMTP("smtp.gmail.com",587)
      server.starttls()
      server.login(user,password)
      server.send_message(msg)
      server.quit()
   except:
      return "False"
   else:
      return "done"
   
def send_acceptance_status(to,fname,lname,age,status):
   try:
      #path=path.replace(" ","%")
      body="Your application for\n"+fname+" "+lname+" Age: "+age+"years\n"+"has been "+status+"\nThank you for using e-Vaccination"
      subject="e-Vaccination Application status"
      msg = EmailMessage()
      msg.set_content(body)
      msg['subject']=subject
      msg['to'] = to

      user = "sarveshgandhere2002@gmail.com"
      msg['from']=user
      password = "kburswetbalyszew"

      server = smtplib.SMTP("smtp.gmail.com",587)
      server.starttls()
      server.login(user,password)
      server.send_message(msg)
      server.quit()
   except:
      return "False"
   else:
      return "done"
