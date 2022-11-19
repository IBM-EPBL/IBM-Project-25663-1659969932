from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from markupsafe import escape
#from flask import Flask 
from flask import flash


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30120;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dwn68713;PWD=Ih2giSrDgrn1cgsY",'','')
#print(conn)
#conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tlf99662;PWD=Xcek6mxqCkEh6uRm", '', '')
print("connection successful...")

app = Flask(__name__)
app.secret_key="123"

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/profile')
def profile():
   return render_template('profile.html')


@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/addstudent')
def new_student():
  return render_template('add_student.html')


@app.route('/formquery')
def query():
   return render_template('form_query.html')

@app.route('/customerlogin',methods=["GET","POST"])
def customerlogin():
   if request.method=='POST':
      cemail=request.form['cemail']
      cpassword=request.form['cpassword']

      sql =f"select * from userss where cemail='{escape(cemail)}' and cpassword='{escape(cpassword)}'"
      stmt = ibm_db.exec_immediate(conn, sql)
      data = ibm_db.fetch_both(stmt)

      if data:
         session["cemail"]=escape(cemail)
         session["cpassword"]=escape(cpassword)
         return redirect("formquery")
      else:
         flash("Username and Password Mismatch","danger")
         return redirect(url_for("index"))
   return render_template('customerlogin.html')

@app.route('/customerregister',methods = ['POST', 'GET'])
def customerregister():
   if request.method == 'POST':
      try:
         cname = request.form['cname']
         cemail = request.form['cemail']
         cpassword = request.form['cpassword']
         cconfirmpassword = request.form['cconfirmpassword']

      
         #insert_sql ="INSERT INTO userss(cname,cemail,cpassword,cconfirmpassword)VALUES(?,?,?,?)"
         insert_sql = "INSERT INTO userss VALUES (?,?,?,?)"
         prep_stmt = ibm_db.prepare(conn,insert_sql)
         ibm_db.bind_param(prep_stmt,1,cname)
         ibm_db.bind_param(prep_stmt,2,cemail)
         ibm_db.bind_param(prep_stmt,3,cpassword)
         ibm_db.bind_param(prep_stmt,4,cconfirmpassword)
         ibm_db.execute(prep_stmt)
         flash("Register successfully","success")        
      except:
         flash("Error","danger")
      finally:
         return redirect(url_for("index"))
         con.close()
   return render_template('customerregister.html')

@app.route('/adminlogin',methods=["GET","POST"])
def adminlogin():
   if request.method=='POST':
      cemail=request.form['cemail']
      cpassword=request.form['cpassword']

      sql =f"select * from admin where cemail='{escape(cemail)}' and cpassword='{escape(cpassword)}'"
      stmt = ibm_db.exec_immediate(conn, sql)
      data = ibm_db.fetch_both(stmt)

      if data:
         session["cemail"]=escape(cemail)
         session["cpassword"]=escape(cpassword)
         return redirect("list")
      else:
         flash("Username and Password Mismatch","danger")
         return redirect(url_for("index"))
   return render_template('adminlogin.html')


@app.route('/agentregister',methods = ['POST', 'GET'])
def agentregister():
   if request.method == 'POST':
      try:
         cname = request.form['cname']
         cemail = request.form['cemail']
         cpassword = request.form['cpassword']
         cconfirmpassword = request.form['cconfirmpassword']
         cidentity=request.form['cidentity']

      
         #insert_sql ="INSERT INTO userss(cname,cemail,cpassword,cconfirmpassword)VALUES(?,?,?,?)"
         insert_sql = "INSERT INTO agent VALUES (?,?,?,?,?)"
         prep_stmt = ibm_db.prepare(conn,insert_sql)
         ibm_db.bind_param(prep_stmt,1,cname)
         ibm_db.bind_param(prep_stmt,2,cemail)
         ibm_db.bind_param(prep_stmt,3,cpassword)
         ibm_db.bind_param(prep_stmt,4,cconfirmpassword)
         ibm_db.bind_param(prep_stmt,5,cidentity)

         ibm_db.execute(prep_stmt)
         
       
         flash("Register successfully","success")        
      except:
         flash("Error","danger")
      finally:
         return redirect(url_for("index"))
         con.close()
   return render_template('agentregister.html')


@app.route('/agentlogin',methods=["GET","POST"])
def agentlogin():
   if request.method=='POST':
      cemail=request.form['cemail']
      cpassword=request.form['cpassword']
      cidentity=request.form['cidentity']

      sql =f"select * from agent where cemail='{escape(cemail)}' and cpassword='{escape(cpassword)}' and cidentity='{escape(cidentity)}'"
      stmt = ibm_db.exec_immediate(conn, sql)
      data = ibm_db.fetch_both(stmt)

      if data:
         session["cemail"]=escape(cemail)
         session["cpassword"]=escape(cpassword)
         session["cidentity"]=escape(cidentity)
         return redirect("agent_view")
      else:
         flash("Username and Password Mismatch","danger")
         return redirect(url_for("prompt_error"))
   return render_template('agentlogin.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    query = request.form['pin']
    email=request.form['email']
  
    sql = "SELECT * FROM students WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('list.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO students VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, address)
      ibm_db.bind_param(prep_stmt, 3, city)
      ibm_db.bind_param(prep_stmt, 4, query)
      ibm_db.execute(prep_stmt)
    

      insert_sql = "INSERT INTO dumm VALUES (?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, address)
      ibm_db.bind_param(prep_stmt, 3, city)
      ibm_db.bind_param(prep_stmt, 4, query)
      ibm_db.bind_param(prep_stmt,5,email)
      
      ibm_db.execute(prep_stmt)
    return render_template('index.html', msg="Student Data saved successfuly..")

@app.route('/list')
def list():
  students = []
  sql = "SELECT * FROM Students"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    students.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if students:
    return render_template("list.html", students = students)


@app.route('/agent_view')
def view():
  students = []
  sql = "SELECT * FROM dumm"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    students.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if students:
    return render_template("agent_view.html", students = students)

@app.route('/delete/<name>')
def delete(name):
  sql = f"SELECT * FROM Students WHERE name='{escape(name)}'"
  print(sql)
  stmt = ibm_db.exec_immediate(conn, sql)
  student = ibm_db.fetch_row(stmt)
  print ("The Name is : ",  student)
  if student:
    sql = f"DELETE FROM Students WHERE name='{escape(name)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)

    students = []
    sql = "SELECT * FROM Students"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
      students.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if students:
      return render_template("list.html", students = students, msg="Delete successfully")


  
  # # while student != False:
  # #   print ("The Name is : ",  student)

  # print(student)
  return "success..."


@app.route('/deletes/<name>')
def deletes(name):
  sql = f"SELECT * FROM dumm WHERE name='{escape(name)}'"
  print(sql)
  stmt = ibm_db.exec_immediate(conn, sql)
  student = ibm_db.fetch_row(stmt)
  print ("The Name is : ",  student)
  if student:
    sql = f"DELETE FROM dumm WHERE name='{escape(name)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)

    students = []
    sql = "SELECT * FROM dumm"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
      students.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if students:
      return render_template("agent_view.html", students = students, msg="ticket solved successfully")


  
  # # while student != False:
  # #   print ("The Name is : ",  student)

  # print(student)
  return "success..."

if __name__ == '__main__':
   app.run(debug = True)


