from flask import Flask, render_template
import Landlord
import Request
import Tenant

app = Flask(__name__)

@app.route('/')

@app.route('/home')
def home():
   return render_template('index.html')

@app.route("/tenantLogIn",methods=['GET','POST'])
def tenantLogIn():
   
   
   return render_template('TenantGUI.html')

@app.route("/landlordLogIn",methods=['GET','POST'])
def landlordLogIn():
  
  
   return render_template('landlordGUI.html')
if __name__ == '__main__':

   app.run(debug=True)

def initialStart():
   tenant1=Tenant("John Smith","123 ABC lane","101",3500)
   tenant2=Tenant("John Doe","123 ABC lane","102",3200)
   tenant3=Tenant("Jane Smith","145 XYZ lane","301",4500)

   return tenant1,tenant2,tenant3