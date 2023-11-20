class Rectangle:
    def __init__(self, top_left_x, top_right_y, bottom_right_x, bottom_left_y):
        self.top_left_x = top_left_x
        self.top_right_y = top_right_y
        self.bottom_right_x = bottom_right_x
        self.bottom_left_y = bottom_left_y

    def to_dict(self):
        return {
            "top_left_x": self.top_left_x,
            "top_right_y": self.top_right_y,
            "bottom_right_x": self.bottom_right_x,
            "bottom_left_y": self.bottom_left_y,
        }
