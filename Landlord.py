
import Building

class Landlord():
    def __init__(self, buildings:int):
        self.buildingList[buildings]=[]
        return
    def addBuilding(self, building:Building):
        self.buildingList.append(building)
        return 
    def generateReport(self):    
        return 
    def getRentAmount(self):
        return self.rentAmount