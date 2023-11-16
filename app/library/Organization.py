import json
from Room import Room
from Event import Event
from Reservation import Reservation

# Exceptions not handled

class Organization:
    def __init__(self, owner, name, map):
        self.owner = owner
        self.name = name
        self.map = map
        self.rooms = {1: Room(9,45,11,3,6), 2: Room(23,435,123,14,66)}
        self.reservations = {}

    def get(self):
        val = {
            "owner": self.owner,
            "name": self.name,
            "map": self.map, 
        }
        return json.dumps(val, indent= 3)
    
    def update(self, **kw):
        for key, value in kw.items(): 
            setattr(self, key, value)

    def delete(self):
        pass

    def getRoom(self, id):
        return self.rooms[id]
    
    def updateRoom(self, id, **kw):
        self.rooms[id].update(kw)

    def deleteRoom(self, id):
        del self.rooms[id]

    def reserve(self, event, room, start):
        #if self.reservations[]
        pass

#   Assuming rectangle consists of x1,x2,y1,y2 attributes and they correspond to:
#   
# x1,y1 _____________
#      |             |
#      |             |
#      |_____________| x2,y2

    def findRoom(self, event, rect, start, end):
        availableRooms = []
        for i in self.rooms.values():
            if rect.x1 <= i.x and rect.x2 >= i.x and rect.y1 <= i.y and rect.y2 >= i.y and event.capacity >= i.capacity:
                noConflict = False
                #for j in self.reservations[]



