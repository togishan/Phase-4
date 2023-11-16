class HourMinute:
    def __init__(self, hour: int, minute: int):
        self.hour = hour
        self.minute = minute

    def to_dict(self) -> dict:
        return {
            "hour": self.hour,
            "minute": self.minute,
        }
