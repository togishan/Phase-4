import json

class Room:
    def __init__(self, x, y, capacity, workingHours, permissions):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.workingHours = workingHours
        self.permissions = permissions
    
    def get(self):
        val = {
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity,
            "workingHours": self.workingHours,
            "permissions": self.permissions
        }
        return json.dumps(val, indent= 3)

    def update(self, **kw):
        for key, value in kw.items(): 
            setattr(self, key, value)


    def delete(self):
        pass
 

#a = Room(5,15,35,12,9)
#print(a.get())
#a.update(x = 33, capacity = 11, permissions = 55, y = 1, randomThing = 88)
#print(a.get())
#print(a.get())