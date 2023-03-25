import os
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import send_mail
from socket import gethostname,gethostbyname

def generate_certificate(name,diseas,doctor,to):
    # Load the certificate template image
    font_size=75
    cert_template_path = "D:\\Projects\\OPD\\static\\certificate.png"
    output_folder = "D:\\Projects\\OPD"
    font= "D:\\Projects\\External_downloads\\Fonts\\dino_and_friend\\Aboreto-Regular.ttf"
    line_font="D:\\Projects\\External_downloads\\Fonts\\dino_and_friend\\Raleway-Black.ttf"
    line=diseas+" has been declared fit."
    line_font_size=45
    doctor_font="D:\\Projects\\External_downloads\\Fonts\\dino_and_friend\\Raleway-VariableFont_wght.ttf"
    doctor_font_size=45

    
    cert_template = Image.open(cert_template_path)

    # Define the text to be added to the certificate
    text = name

    # Determine the font size and thickness based on user input
    font_scale = int(font_size * 0.75)  # Pillow font size is in points, not pixels
    font_thickness = int(font_size * 0.05)  # You can adjust this as needed
    line_font_scale=int(line_font_size*0.75)
    doctor_font_scale=int(doctor_font_size*0.75)
    #line_font_thickness=

    # Load the font
    if font.lower() == "default":
        font = ImageFont.load_default()
    else:
        # Load a custom font file
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), font)
        font = ImageFont.truetype(font_path, size=font_scale)
        line_font_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), line_font)
        line_font = ImageFont.truetype(line_font_path, size=line_font_scale)
        doctor_font_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), doctor_font)
        doctor_font = ImageFont.truetype(doctor_font_path, size=doctor_font_scale)

    # Get the size of the text
    text_size = font.getsize(text)
    line_size= line_font.getsize(line)
    doctor_size=doctor_font.getsize(doctor)

    # Calculate the coordinates of the text
    x = (cert_template.width - text_size[0]) // 2
    y = (cert_template.height - text_size[1]) // 2
    y=320

    x1=(cert_template.width - line_size[0]) // 2
    y1=435

    
    x2=275-(doctor_size[0]//2)
    y2=525

    # Add the text to the image
    print(line)
    draw = ImageDraw.Draw(cert_template)
    draw.text((x, y), text, font=font, fill="black")
    draw.text((x1,y1),line,font=line_font,fill=(0,0,0))
    draw.text((x2,y2),doctor,font=doctor_font,fill=(0,0,0))

    # Save the certificate with a new filename
    #output_path = os.path.join(output_folder, f"{name}_certificate.png")
    #cert_template.save(f"{name}_certificate.png")
    cert_template.save("static/certificates/"+name+"_certificate.pdf")
    #send_mail.send_certificate_link("http://"+gethostbyname(gethostname())+":5000/certificate/"+name+"_certificate.pdf",to)
    send_mail.send_certificate_link(gethostbyname(gethostname())+":5000/certificate",to)

    #print(f"Certificate for '{name}' saved to {}")


#print(get_font("D:\\Projects\\External_downloads\\Fonts\\static"))



name = "John Doe"
font_size = 75
#font = "D:\\Projects\\External_downloads\\Fonts\\static\\Raleway-Black.ttf"
#pre(name, font_size, "Dino And Friend-Texture1.ttf", cert_template_path)
#generate_certificate(name, "headech","Sarvesh Gandhere")
