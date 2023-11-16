class HourMinute:
    def __init__(self, hour: int, minute: int):
        self.hour = hour
        self.minute = minute

    def get(self):
        val = {
            "hour": self.hour,
            "minute": self.minute,
        }
        return val
