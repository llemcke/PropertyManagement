import Tenant
class Request():
    def __init__(self,tenant:Tenant,description:str,time:str):
        self.tenant=tenant
        self.description=description
        self.time=time
        self.status=False
        return
    def resolve(self):
        self.status=True
        