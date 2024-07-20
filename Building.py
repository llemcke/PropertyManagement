import Tenant

class Building:
     def __init__(self, address:str):
        self.address=address
        self.tenants=[]
        return