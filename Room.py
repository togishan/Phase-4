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
 

 
