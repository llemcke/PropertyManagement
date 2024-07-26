from flask import Flask, render_template,request,session,redirect, url_for
import os
from supabase import create_client, Client
from Landlord import Landlord
from RepairRequest import RepairRequest
from Tenant import Tenant
app = Flask(__name__)
app.secret_key = os.urandom(24) 

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.route('/')

@app.route('/home')
def home():
   return render_template('index.html')
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('tenant', None)
    session.pop('landlord', None) 
    return redirect(url_for('home'))  
@app.route("/tenantLogIn",methods=['GET','POST'])
def tenantLogIn(): 
   '''
   Authenticates login. Checks User table for existing username and ensures password matches that username. 
   Returns True if existing username and matching password, otherwise False
   '''
   if request.method == 'POST':
      username = request.form.get('username')
      password = request.form.get('password')
      
      response = supabase.table('User').select('*').eq('username', username).execute()
      
      if len(response.data) == 0:
         # Username does not exist
         return render_template('index.html', message="Username does not exist")
         
      # Get the first user record
      user = response.data[0]

      # Check if the password matches and that user is a Tenant
      if user['password'] == password and user.get('isTenant'): 
         #Get the tenant info
         tenant_response = supabase.table('Tenant').select('*').eq('user_id', user['user_id']).execute()

         tenant = tenant_response.data[0]
         #Find the building info of the tenant
         building_response = supabase.table('Building').select('address').eq('building_id', tenant['building']).execute()

               
         building = building_response.data[0]
         buildingAddress = building['address']
         
         owing = tenant['rent_owing']
         
         #Create tenant Object
         tenant_obj = Tenant(
         userID=tenant['user_id'],
         first_name=tenant['first_name'],
         last_name=tenant['last_name'],
         address=buildingAddress,
         unit=tenant['unit'],
         rentAmount=tenant['rent_amount']
         )
         #Store session data
         session['tenant'] = {
         'userID': tenant_obj.ID,
         'firstName': tenant_obj.firstName,
         'lastName': tenant_obj.lastName,
         'address': tenant_obj.address,
         'unit': tenant_obj.unit,
         'rentAmount': tenant_obj.rentAmount,
         'rentOwed':owing
        }

         
                         
         return redirect(url_for('tenantDisplay'))
      else:
         return render_template('index.html', message="Invalid credentials or not a tenant")

@app.route("/landlordLogIn",methods=['GET','POST'])
def landlordLogIn():
   '''
   Authenticates login. Checks User table for existing username and ensures password matches that username. 
   Returns True if existing username and matching password, otherwise False
   '''
   if request.method == 'POST':
      username = request.form.get('usernameL')
      password = request.form.get('passwordL')
      
      #Search for user
      response = supabase.table('User').select('*').eq('username', username).execute()
      
      if len(response.data) == 0:
         # Username does not exist
         return render_template('index.html', message="Username does not exist")
         
      # Get the first user record
      user = response.data[0]

      # Check if the password matches and that user is a Landlord
      if user['password'] == password and user.get('isTenant')==False: 
          
         response = supabase.table('Landlord').select('*').eq('user_id', user['user_id']).execute()
         landlord=response.data[0]
         building_response = supabase.table('Building').select('*').eq('owned_by', landlord['user_id']).execute()

         #Create a landlord object
         landlord_obj = Landlord(
         userID=landlord['user_id'],
         firstName=landlord['first_name'],
         lastName=landlord['last_name'],
         buildingList=building_response.data
         ) 

         #Store session data
         session['landlord'] = {
         'userID': landlord_obj.ID,
         'firstName': landlord_obj.firstName,
         'lastName': landlord_obj.lastName
         }
                                 
         return redirect(url_for('landlordDisplay'))
   else:
      return render_template('index.html', message="Invalid credentials or not a tenant")
   

@app.route("/makePayment",methods=['GET','POST'])
def makePayment():
   '''
   Allows tenant to make payment
   '''
   if request.method == 'POST':
      #Create tenant object using session data
      tenant_obj = Tenant(
      userID=session['tenant']['userID'],
      first_name=session['tenant']['firstName'],
      last_name=session['tenant']['lastName'],
      address=session['tenant']['address'],
      unit=session['tenant']['unit'],
      rentAmount=session['tenant']['rentAmount']
      )

      amount_str = request.form.get('payAmount')
      amount=float(amount_str)

      #Call method to update rent
      new_owing=tenant_obj.updateRentOwed(supabase,amount)
      #Update session info
      session['tenant']['rentOwed']=new_owing
   
      return redirect(url_for('tenantDisplay'))
   return

@app.route("/createRequest",methods=['GET','POST'])
def createRequest():
   '''
   Allow tenant to create a request
   '''
   if request.method == 'POST':
      description = request.form.get('requestDescription')
      
      #Create a tenant object using session data
      tenant_obj = Tenant(
      userID=session['tenant']['userID'],
      first_name=session['tenant']['firstName'],
      last_name=session['tenant']['lastName'],
      address=session['tenant']['address'],
      unit=session['tenant']['unit'],
      rentAmount=session['tenant']['rentAmount']
      )
        
      #Create request object
      req = RepairRequest(tenant=tenant_obj,description=description,status=False)
        
      # Call the method to create a new request in the database
      req.newRequest(supabase)

      return redirect(url_for('tenantDisplay'))
   return

@app.route("/adjustTenants",methods=['GET','POST'])
def adjustTenants():
   if request.method == 'POST':

      #get info from front end
      tenantID=request.form.get('tenantID')
      rentAmount =float( request.form.get('rentAmount'))
      rentOwing = float(request.form.get('rentOwing'))

      #update tenant's rent in database
      supabase.table('Tenant').update({
      'rent_amount':rentAmount,
      'rent_owing':rentOwing
      }).eq('user_id', tenantID).execute()
        
      return redirect(url_for('landlordDisplay'))
   else:
      return render_template('index.hmtl')
@app.route('/tenantDisplay')
def tenantDisplay():
   '''
   Used to display all info for the tenant dashboard
   '''
   repair_response = supabase.table('Requests').select('*').eq('tenant_id', session['tenant']['userID']).execute()
   return render_template('TenantGUI.html',tenant=session['tenant'],owing=session['tenant']['rentOwed'],requests=repair_response.data)

@app.route('/landlordDisplay', methods=['GET'])
def landlordDisplay():
   '''
   Used to display all info for the landlord dashboard
   '''
   #retrive landlord ID and fins list of buildings
   landlord_id = int(session['landlord'].get('userID'))
   building_response = supabase.table('Building').select('*').eq('owned_by', landlord_id).execute()
   
   #Create landlord object
   landlord_obj = Landlord(
   userID=landlord_id,
   firstName=session['landlord'].get('firstName'),
   lastName=session['landlord'].get('lastName'),
   buildingList=building_response.data
   )

   # Get all data for tenants and repairs
   tenantList=landlord_obj.getTenantList(supabase)
   rentTotal=landlord_obj.getRentTotal(tenantList)  
   repairs=landlord_obj.getRequests(supabase,tenantList)
   status = request.args.get('requestStatus', 'All')
   #Take the repair list and store the ones requested by user
   repairList=[]
   if status == 'Open':
        for repair in repairs:
           if not repair['resolved']:
              repairList.append(repair)
   elif status == 'Resolved':
         for repair in repairs:
           if repair['resolved']:
              repairList.append(repair)
   else:
         for repair in repairs:
            repairList.append(repair)
    
   #Render the template with all info
   return render_template('LandlordGUI.html',selected_status=status,landlord=landlord_obj,buildings=building_response.data,tenant=tenantList,rentTotal=rentTotal,repairs=repairList)

@app.route("/changeStatus",methods=['GET','POST'])
def changeStatus():
   '''
   Allows the landlord to change the status of a request
   '''
   #Retrieve request ID and search for it in database
   requestID = request.form.get('requestID')
   response = supabase.table("Requests").select("resolved").eq("request_id", requestID).single().execute()
   
   #toggle status
   current_status = response.data['resolved']
   new_status = not current_status
   #change the request status        
   response = (supabase.table("Requests").update({"resolved": new_status}).eq("request_id", requestID).execute() )
   return redirect(url_for('landlordDisplay'))


if __name__ == '__main__':

   app.run(debug=True)
