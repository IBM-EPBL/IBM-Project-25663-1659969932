
#  login and register page 

# CONNECTED WITH IBM DB login and register page 



Working with IBM Db2 service 

--- ADD IT IN YOUR PYTHON APP ---
> import ibm_db
> conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=<HOSTNAME>;PORT=<PORTNUMBER>;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;
> UID=<USERNAME>;PWD=<PASSWORD>",'','')
> print(conn)
> print("connection successful...")


Open the application

http://127.0.0.1:5000/
