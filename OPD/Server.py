from flask import Flask, render_template, request,send_file
from send_mail import *
from random import randint
from DB_module import *
from socket import gethostname,gethostbyname
import cert
import os

app=Flask(__name__)

session_otp_id=[]


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/user")
def user():
    return render_template("/user_side/user_index.html")

@app.route("/user_login")
def userl():
    return render_template("/user_side/user_login.html")

@app.route("/user_panel")
def user_panel():
    return render_template("/user_side/user_panel.html")

@app.route("/add_member_panel")
def add_member_panel():
    return render_template("/user_side/add_member.html")

@app.route("/send_otp/",methods=["POST"])
def controll_car():
    global session_otp_id
    req=request.get_json()
    session_id=randint(1111111,99999999999999)
    otp=send_email_otp(req["email"])
    if (otp=="False"):
        return "False"
    session_otp_id.append({"email":req["email"],"session_id":session_id,"otp":otp})
    return {"otp":str(otp),"session_id":session_id}

@app.route("/login_admin")
def login_admin():
    return render_template("login_admin.html")

@app.route('/vadapav/<filename>')
def download_image(filename):
    # Set the filename and mimetype of the file
    filename="static/certificates/"+filename+"_certificate.pdf"
    print(filename)
    if(os.path.isfile(filename)==True):
        mimetype = 'application/pdf'
        return send_file(filename, mimetype=mimetype, as_attachment=True, attachment_filename='downloaded-pdf.pdf')
    else:
        return "File not exists"
    #filename="static/certificates/"+filename
    
    # Use the send_file function to send the file
    
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("new_admin_page.html")

@app.route("/doctor_dashboard")
def doctor_dashboard():
    return render_template("temp.html")

@app.route("/add_doctor_form")
def add_doctor_form():
    return render_template("add_doctor_form.html")

@app.route("/add_patient_form")
def add_patient_form():
    return render_template("add_patient_form.html")

@app.route("/treat_parent")
def treat_parent():
    return render_template("patients_tratment_form.html")

@app.route("/requests")
def requestststtstttst():
    return render_template("request_member.html")


@app.route("/add_vaccine_form")
def add_vaccine_form():
    return render_template("add_vaccine_form.html")

@app.route("/update_vaccine")
def update_vaccine():
    return render_template("update_vaccine.html")

@app.route("/certificate")
def certificate():
    print("certificate")
    return render_template("certificate.html")

# @app.route("/center_registration_form")
# def crf():
#     return render_template("center_registration_form.html")

@app.route("/Main_content")
def mc():
    return render_template("Main_content.html")

# @app.route("/center_panel")
# def center_panel():
#     return render_template("center_panel.html")


@app.route("/check_otp/",methods=["POST"])
def check_otp():
    global session_otp_id
    print("cheking otp")
    req=request.get_json()
    print("printing req: ",req)
    con=False
    for i in session_otp_id:
        print({"email":req["email"],"session_id":int(req["session_id"]),"otp":req["otp"]})
        if(i=={"email":req["email"],"session_id":int(req["session_id"]),"otp":req["otp"]}):
            print("found session")
            db=handle_data()
            print("below line commented")
            # result=db.save_new_user(req["email"],req["name"])
            print("above line commented")
            session_otp_id.remove(i)
            ret = db.check_exists(req["email"])
            print(ret)
            if ret=="found":
               return "true"
            return "false"
        else:
            print("not found")
            return "not found"
        
@app.route("/add_doctor/",methods=["post"])
def add_doctor():
    req=request.get_json()
    db=handle_data()
    ret=db.add_doctor(req["fname"],req["lname"],req["age"],req["gender"],req["phone"],req["mail"],req["spacialist"],req["img"])
    return ret


@app.route("/add_patient/",methods=["post"])
def add_patient():
    req=request.get_json()
    db=handle_data()
    ret=db.add_patient(req["fname"],req["lname"],req["age"],req["gender"],req["phone"],req["mail"],req["weight"],req["height"],req["blood"],req["problem"],req["dieses"],req["allocate"])
    return ret

@app.route("/add_member/",methods=["post"])
def add_member():
    req=request.get_json()
    db=handle_data()
    ret=db.add_member(req["fname"],req["lname"],req["age"],req["gender"],req["phone"],req["mail"],req["weight"],req["height"],req["blood"],req["problem"])
    return ret

@app.route("/get_doctors/",methods=["post"])
def get_doctors():
    req=request.get_json()
    db=handle_data()
    ret=db.get_doctors()
    return {"ret":ret}

@app.route("/get_Patinet_status/",methods=["post"])
def get_ps():
    req=request.get_json()
    mail=req["mail"]
    db=handle_data()
    ret=db.get_Patinet_status(mail)
    return {"ret":ret}


@app.route("/download_certificate/",methods=["post"])
def download_certificate():
    req=request.get_json()
    mail=req["mail"]
    fname=req["fname"]
    lname=req["lname"]
    db=handle_data()
    ret=db.download_certificate(mail,fname,lname)
    if ret=="found":
        #filename="static/certificates/"+fname+" "+lname+"_certificate.pdf"
        #print(filename)
        #mimetype = 'application/pdf'
        #return send_file(filename, mimetype=mimetype, as_attachment=True, attachment_filename='downloaded-pdf.pdf')
        return "done"
    return "error"

@app.route("/get_patients/",methods=["post"])
def get_patients():
    req=request.get_json()
    db=handle_data()
    ret=db.get_patients()
    return {"ret":ret}

@app.route("/get_requests/",methods=["post"])
def get_req():
    req=request.get_json()
    db=handle_data()
    ret=db.get_requests()
    return {"ret":ret}

@app.route("/get_patient_doctor/",methods=["post"])
def get_patient_doctorr():
    req=request.get_json()
    doctor=req["doctor"]
    db=handle_data()
    ret=db.get_patient_doctor(doctor)
    return {"ret":ret}

@app.route("/set_patient_treatment_form/",methods=["post"])
def set_patient_treatment_form():
    req=request.get_json()
    lname=req["lname"]
    fname=req["fname"]
    phone=req["phone"]
    db=handle_data()
    ret=db.set_patient_treatment_form(lname,fname,phone)
    return {"ret":ret}


@app.route("/delete_member/",methods=["post"])
def delete_member():
    req=request.get_json()
    lname=req["lname"]
    fname=req["fname"]
    age=req["age"]
    gender= req["gender"]
    mail=req["mail"]
    phone=req["phone"]
    db=handle_data()
    ret=db.delete_member(fname,lname,age,gender,phone,mail)
    if(req["action"]=="accept"):
        sm=send_acceptance_status(mail,fname,lname,age,"Accepted")
    elif(req["action"]=="rejected"):
        sm=send_acceptance_status(mail,fname,lname,age,"Rejected")
    return {"ret":ret}



@app.route("/submit_treatment/",methods=["post"])
def submit_treatment():
    req=request.get_json()
    print(req)
    lname=req["lname"]
    fname=req["fname"]
    phone=req["phone"]
    desc=req["desc"]
    note=req["note"]
    meds=req["med"]
    vaccine=req["vaccine"]
    status=req["status"]
    diseas=req["diseas"]
    doctor=req["doctor"]
    to=req["to"]
    db=handle_data()
    ret=db.submit_treatment(lname,fname,phone,note,meds,vaccine,status,diseas)
    if(ret=="done"):
        if(status=="done"):
            db.dec_vaccine(vaccine)
            cert.generate_certificate(fname+" "+lname, diseas,doctor,to)
        ret=db.update_patient(lname,fname,phone,desc,status)
        return {"ret":ret}
    return {"ret":False}


@app.route("/upadate_treatment_patient/",methods=["post"])
def upadate_treatment_patient():
    req=request.get_json()
    print(req)
    db=handle_data()
    lname=req["lname"]
    fname=req["fname"]
    mail=req["mail"]
    ret=db.upadate_treatment_patient(mail,fname,lname)
    return(ret)

@app.route("/upadate_vaccine_slot/",methods=["post"])
def upadate_vaccine_slot():
    req=request.get_json()
    print(req)
    db=handle_data()
    name=req["name"]
    count=req["count"]
    ret=db.upadate_vaccine_slot(name,count)
    return(ret)


@app.route("/get_graph_data/",methods=["post"])
def get_graph_data():
    db=handle_data()
    ret=db.get_graph_data()
    return {"ret":ret}

# @app.route("/submit_form_center/",methods=["POST"])
# def sbfc():
#     req=request.get_json()
#     print(req)
#     db=handle_data()
#     ret=db.save_new_Center(req["center_name"],req["mailid"],req["center_city"],req["center_district"],req["center_state"])
#     print(ret)
#     return "true"

# @app.route("/get_centers/",methods=["POST"])
# def gc():
#     req=request.get_json()
#     db=handle_data()
#     print(req["mail"])
#     ret=db.get_centers(req["mail"])
#     ret1=jsonify({"ret":ret})
#     print("This is from get centers",ret1)
#     return ret1


@app.route("/addv/",methods=["POST"])
def addv():
    req=request.get_json()
    db=handle_data()
    ret=db.savev(req["name"],req["desc"],req["count"])
    print(ret)
    return ret


@app.route("/get_vaccine/",methods=["POST"])
def gv():
    req=request.get_json()
    db=handle_data()
    ret=db.get_vaccine()
    return {"ret":ret}


app.run(host=gethostbyname(gethostname()))





