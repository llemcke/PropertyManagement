import System
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
    
    def updateRentOwed(self,rentPaid:float,):
        '''
        handles when rent payment is made by tenant
        '''
        supabase = System.get_client.get_client()
        response = (
        supabase.table("Tenant")
        .update({"rent_owing": self.rentAmount-rentPaid})
        .eq("user_id", self.ID)
        .execute()
        )