# rect is defined as (x0,y0,x1,y1) x0, y0 are the coordinates of the bottom left corner. 
# Top right corner will be x1, y1
# x1 >= x0 and y1 >= y0
class Rectangle:
    def __init__(self, bottom_left_x, bottom_left_y, top_right_x, top_right_y):
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y
        
    def to_dict(self):
        return {
            "bottom_left_x": self.bottom_left_x,
            "bottom_left_y": self.bottom_left_y,
            "top_right_x": self.top_right_x,
            "top_right_y": self.top_right_y,
        }
