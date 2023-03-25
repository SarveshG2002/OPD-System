import mysql.connector
from datetime import date
import random

class handle_data():
    __mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="vaccination")
    __mycursor = __mydb.cursor()

    def save_new_user(self,mailid,name):
        #query="insert into login_data values (%s, %s, %s, %s, %s)"
        query="select * from login_data where mailid=%s"
        value=(mailid,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        if result==[]:
            query="insert into login_data values(%s,%s)"
            value=(mailid,name,)
            self.__mycursor.execute(query,value)
            self.__mydb.commit()
            print("data inserted")
            return "new User"
        else:
            query="select * from centers where mailid=%s"
            value=(mailid,)
            self.__mycursor.execute(query,value)
            result=self.__mycursor.fetchall()
            return result
        
    def download_certificate(self,email,fname,lname):
        query="select fname,lname from patient where mail=%s && fname=%s && lname=%s"
        value=(email,fname,lname)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        if result==[]:
            return "not found"
        else:
            return "found"
        
    def check_exists(self,email):
        query="select fname from doctors where mail=%s"
        value=(email,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        #print(result)
        if result==[]:
            return "not found"
        else:
            return "found"
            

    
    def add_doctor(self,fname,lname,age,gender,phone,mail,spacialist,img):
        query="insert into doctors values (%s, %s, %s, %s,%s,%s,%s,%s)"
        value=(fname,lname,age,gender,phone,mail,spacialist,img,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        return "doctor added"
    
    def add_patient(self,fname,lname,age,gender,phone,mail,weight,height,blood,problem,dieses,allocate):
        today=date.today()
        query="insert into patient values (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        value=(fname,lname,age,gender,phone,mail,weight,height,blood,problem,dieses,allocate,"",today)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        return "patient added"
    
    def add_member(self,fname,lname,age,gender,phone,mail,weight,height,blood,problem):
        query="insert into temp_member values (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"
        value=(fname,lname,age,gender,phone,mail,weight,height,blood,problem)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        return "patient added"
    
    def delete_member(self,fname,lname,age,gender,phone,mail):
        query="delete from temp_member where fname=%s && lname=%s && age=%s && gender=%s && phone=%s && mail=%s"
        value=(fname,lname,age,gender,phone,mail)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        return "patient deleted"

    def savev(self,vname,desc,count):
        query="insert into vaccine values (%s, %s, %s)"
        value=(vname,desc,count)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        return "added"
    
    def get_doctors(self):
        query="select * from doctors"
        self.__mycursor.execute(query)
        result=self.__mycursor.fetchall()
        return result
    
    
    def get_patient_doctor(self,mail):
        query="select * from patient where allocate='"+mail+"'"
        self.__mycursor.execute(query)
        result=self.__mycursor.fetchall()
        return result
    
    def set_patient_treatment_form(self,lname,fname,phone):
        #query="select * from treatment where lname='"+lname+"' && fname='"+fname+"' && phone='"+phone+"'"
        query=" select * from treatment where phone=%s && lname=%s && fname=%s"
        print(query)
        value=(phone,fname,lname)
        print(value)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        return result
    
    def get_Patinet_status(self,mail):
        query="select fname,lname,problem,allocate,treatment from patient where mail='"+mail+"'"
        #print(query)
        value=(mail)
        #print(value)
        self.__mycursor.execute(query)
        result=self.__mycursor.fetchall()
        return result
    
    def get_patients(self):
        query="select * from patient"
        self.__mycursor.execute(query)
        result=self.__mycursor.fetchall()
        return result
    
    def get_requests(self):
        query="select * from temp_member"
        self.__mycursor.execute(query)
        result=self.__mycursor.fetchall()
        return result
    
    def get_vaccine(self):
        query="select * from vaccine"
        self.__mycursor.execute(query)
        result=self.__mycursor.fetchall()
        return result
    
    def get_graph_data(self):
        query="select date from patient"
        self.__mycursor.execute(query)
        result=self.__mycursor.fetchall()
        return result
    
    def submit_treatment(self,lname,fname,phone,note,meds,vaccine,status,diseas):
        query="select * from treatment where phone=%s && fname=%s"
        value=(phone,fname,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        print("treatment: ",result)
        if result==[]:
            print("storing new user")
            query="insert into treatment values (%s, %s, %s, %s, %s ,%s ,%s, %s )"
            value=(lname,fname,phone,note,meds,vaccine,status,diseas)
            self.__mycursor.execute(query,value)
            self.__mydb.commit()
        else:
            self.update_data(lname,fname,phone,note,meds,vaccine,status,diseas)
        return "done"
        
    def update_data(self,lname,fname,phone,note,meds,vaccine,status,diseas):
        print("updating user")
        query="update treatment set note='"+note+"' , meds='"+meds+"' , vaccine='"+vaccine+"' , status='"+status+"', diseas='"+diseas+"' where lname='"+lname+"' && fname='"+fname+"' && phone='"+phone+"'"
        value=(lname,fname,phone,)
        print(query)
        self.__mycursor.execute(query)
        self.__mydb.commit()
        print(self.__mycursor.rowcount,"records updated")
    
    def dec_vaccine(self,vaccine):
        query="UPDATE vaccine SET count = count - 1 WHERE name='"+vaccine+"'"
        self.__mycursor.execute(query)
        self.__mydb.commit()
        print(self.__mycursor.rowcount,"records updated")



    def update_patient(self,lname,fname,phone,desc,status):
        query="update patient set problem='"+desc+"' , treatment='"+status+"' where lname='"+lname+"' && fname='"+fname+"' && phone='"+phone+"'"
        print(query)
        self.__mycursor.execute(query)
        self.__mydb.commit()
        print(self.__mycursor.rowcount,"records updated")
        return "done"
    
    def upadate_treatment_patient(self,mail,fname,lname):
        query="update patient set treatment='downloaded' where lname='"+lname+"' && fname='"+fname+"' && mail='"+mail+"'"
        print(query)
        self.__mycursor.execute(query)
        self.__mydb.commit()
        print(self.__mycursor.rowcount,"records updated")
        query="update treatment set status='downloaded' where lname='"+lname+"' && fname='"+fname+"'"
        print(query)
        self.__mycursor.execute(query)
        self.__mydb.commit()
        print(self.__mycursor.rowcount,"records updated")
        return "done"
    
    def upadate_vaccine_slot(self,name,count):
        query="update vaccine set count=%s where name='"+name+"'"
        print(query)
        value=(count,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        print(self.__mycursor.rowcount,"records updated")
        return "done"
        

#print(handle_data().get_centers("sarveshgandhere2002@gmail.com"))
