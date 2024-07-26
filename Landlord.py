
import Building

class Landlord():
    def __init__(self, userID,firstName:str, lastName:str, buildingList):
        self.ID=userID
        self.firstName=firstName
        self.lastName=lastName
        self.buildingList=buildingList
        return
    
    def getTenantList(self,supabase):
        '''
        Create a list of tenants that live in the buildings owned by the landlord
        '''
        tenantList = []
        #Generate list of all buildings owned by landlord
        for building in self.buildingList:
            response = supabase.table('Tenant').select('*').eq('building', building['building_id']).execute()
            tenantList.extend(response.data)
        #Generate list of tenants based off of building owned by landlord
        for tenant in tenantList:
            building_response = supabase.table('Building').select('address').eq('building_id', tenant['building']).execute()        
            building = building_response.data[0]
            buildingAddress = building['address']
            tenant['address']=buildingAddress
        return tenantList
    def getRentTotal(self,tenantList):
        '''
        Find rent total for all buildings
        '''
        total = 0
        for tenant in tenantList:
            rent_amount = int(tenant['rent_amount'])
            if rent_amount is not None:
                total += rent_amount
        return total
    def getRequests(self,supabase,tenantList):
        '''
        Find a list of requests for all buildings owned by landlord
        '''
        requests=[]
        #Find requests submitted by each tenant
        for tenant in tenantList:
            response = supabase.table('Requests').select('*').eq('tenant_id', tenant['user_id']).execute()
            tenant_requests=response.data
                    
            building_response = supabase.table('Building').select('address').eq('building_id', tenant['building']).single().execute()
            building_address = building_response.data['address']

            # Need to include the name and address
            for request in tenant_requests:
                request_with_tenant_info = {
                **request,
                'firstName': tenant['first_name'],
                'lastName': tenant['last_name'],
                'address': building_address
                }
                requests.append(request_with_tenant_info)
        return requests
    