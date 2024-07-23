
import os
from Tenant import Tenant

from Request import Request
from supabase import create_client, Client



_client: Client = None

class System():
    def get_client(cls) -> Client:
        if cls._client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            cls._client = create_client(url, key)
        return cls._client
    
    def checkLogin (self,username:str,password:str)->bool:
        '''
        Authenticates login. Checks User table for existing username and ensures password matches that username. 
        Returns True if existing username and matching password, otherwise False
        '''
        supabase = self.get_client.get_client()
        response = supabase.table('User').select('*').eq('username', username).execute()

        # Check if any rows were returned
        if len(response.data) == 0:
            # Username does not exist
            return False

        # Get the first user record
        user = response.data[0]

        # Check if the password matches
        if user['password'] == password:
            return True

        return False
