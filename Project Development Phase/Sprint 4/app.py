from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from markupsafe import escape
#from flask import Flask 
from flask import flash


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lmr68468;PWD=4BNA231psxCisG9V",'','')
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

@app.route('/agent_view')
def view():
   return render_template('agent_view.html')

@app.route('/formquery')
def query():
   return render_template('form_query.html')

@app.route('/assignAgentAdmin')
def viewagent():
   return render_template('assignAgentAdmin.html')


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
    pin = request.form['pin']

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
      ibm_db.bind_param(prep_stmt, 4, pin)
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


@app.route('/assignTickets/<name>')
def assignTicketsAgentAdmin(name):
    if 'loggedin' in session:
        agents = []
        sql = "SELECT AGENTUSERNAME, AGENTEMAILADDRESS, AGENTTICKETS, AGENTTICKETSRESOLVED FROM AGENTS"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            # print ("The Name is : ",  dictionary)
            agents.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)
        if agents:
            return render_template("assignAgentAdmin.html", agents = agents, username = session['ADMINUSERNAME'],ticketid=name)
    return redirect(url_for('adminlog'))


#edit this
@app.route('/assignTicketsAdmin/<ticket>/<username>')
def assignTicketsAdmin(ticket, username):
    if 'loggedin' in session:
        msg=""
        stmt = "UPDATE TICKETS SET STATUS = ?, AGENTUSERNAME = ? WHERE TICKETID = ?"
        prep_stmt = ibm_db.prepare(conn, stmt)
        ibm_db.bind_param(prep_stmt, 1, 'Agent Alloted')
        ibm_db.bind_param(prep_stmt, 2, username)
        ibm_db.bind_param(prep_stmt, 3, ticket)
        ibm_db.execute(prep_stmt)

        stmt = "SELECT cidentity, cemail FROM AGENT WHERE cname=?"
        prep_stmt = ibm_db.prepare(conn, stmt)
        ibm_db.bind_param(prep_stmt, 1, username)
        ibm_db.execute(prep_stmt)
        account = ibm_db.fetch_assoc(prep_stmt)
        agentTicket = account['cidentity']
        emailaddress = account['cemail']
        agentTicket+=1

        stmt = "UPDATE AGENT SET cidentity = ? WHERE cname = ?"
        prep_stmt = ibm_db.prepare(conn, stmt)
        ibm_db.bind_param(prep_stmt, 1, agentTicket)
        ibm_db.bind_param(prep_stmt, 2, username)
        ibm_db.execute(prep_stmt)

       
        agents = []
        sql = "SELECT cname FROM AGENT"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            # print ("The Name is : ",  dictionary)
            agents.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)
        if agents:
            return redirect(url_for('assignTickets'))
    return redirect(url_for('adminlogin'))

if __name__ == '__main__':
   app.run(debug = True)


