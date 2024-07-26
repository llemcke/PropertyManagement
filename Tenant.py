
class Tenant():
    def __init__(self, userID:int,first_name:str,last_name:str, address:str, unit:str, rentAmount:float):
        self.ID=userID
        self.firstName=first_name
        self.lastName=last_name
        self.address=address
        self.unit=unit
        self.rentAmount=rentAmount
        return
    def getAddress(self):
        return self.address
    def getuserID(self):
        return self.ID
    def getUnit(self):
        return self.unit
    def getRentAmount(self):
        return self.rentAmount
    
    def updateRentOwed(self,supabase,rentPaid:float,)->float:
        '''
        handles when rent payment is made by tenant, updates rent owed
        '''
        
        response = supabase.table("Tenant").select('rent_owing').eq("user_id", self.ID).execute()
        user=response.data[0]
        current_owing = user['rent_owing']
        new_owing = current_owing - rentPaid
        supabase.table("Tenant").update({"rent_owing": new_owing}).eq("user_id", self.ID).execute()
        return new_owing
