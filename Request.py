import Tenant
import Request
import System

class Request():
    def __init__(self,tenant:Tenant,description:str,time:str):
        self.tenant=tenant
        self.description=description
        self.time=time
        self.status=False
        return
    def createRequest(self):
      '''
      Allows tenant to submit a repair request. Takes a Request and inserts it into the Requests table
      '''
      supabase = System.get_client.get_client()
      response = (
        supabase.table("Requests")
        .insert({"tenant_id": self.tenant.ID, "description": self.description, "resolved": self.status})
        .execute()
    )  
      return
    def deleteRequest(id:int):
        '''
        Allows tenant to delete a request they've made
        '''
        supabase = System.get_client.get_client()
        response = supabase.table('Requests').delete().eq('id', id).execute()
        return
    def resolveRequest(id:int):
        '''
        For landlord to resolve a request
        '''
        supabase = System.get_client.get_client()
        response = (
        supabase.table("Requests")
        .update({"resolved": "TRUE"})
        .eq("id", id)
        .execute()
        )
        return       