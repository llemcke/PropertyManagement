import Tenant
import RepairRequest


class RepairRequest():
    def __init__(self,tenant:Tenant,description:str,status):
        self.tenant=tenant
        self.description=description
        self.status=status
        return
    def newRequest(self,supabase):
      '''
      Allows tenant to submit a repair request. Takes a Request and inserts it into the Requests table
      '''
      response = (supabase.table("Requests").insert({"tenant_id": self.tenant.ID, "description": self.description, "resolved": self.status}).execute())  
      return
    def deleteRequest(supabase,id:int):
        '''
        Allows tenant to delete a request they've made
        '''
        response = supabase.table('Requests').delete().eq('id', id).execute()
        return
     