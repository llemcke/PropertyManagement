
class Tenant():
    def __init__(self, name:str, address:str, unit:int, rentAmount:int):
        self.name=name
        self.address=address
        self.unit=unit
        self.rentAmount=rentAmount
        return
    def getAddress(self):
        return self.address
    def getUnit(self):
        return self.unit
    def getRentAmount(self):
        return self.rentAmount