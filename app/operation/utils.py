from datetime import datetime, timedelta
from ..models import Event, Room


def are_two_times_conflicting(
    start_time1: datetime,
    end_time1: datetime,
    start_time2: datetime,
    end_time2: datetime,
) -> bool:
    if start_time1 < start_time2:
        return end_time1 > start_time2
    else:
        return start_time1 < end_time2


def is_room_available(room_id: int, start_time: datetime, end_time: datetime) -> bool:
    # TODO : Test with conflicts
    room = Room.get(Room.id == room_id)
    events_in_room = Event.select().where(Event.location_id == room_id)

    # Is room open?
    if not (
        (
            (
                start_time.hour == room.open_time.hour
                and start_time.minute >= room.open_time.minute
            )
            or (start_time.hour > room.open_time.hour)
        )
        and (
            (
                end_time.hour == room.close_time.hour
                and end_time.minute <= room.close_time.minute
            )
            or (end_time.hour < room.close_time.hour)
        )
    ):
        return False

    # Is room available?
    for each in events_in_room:
        if each.weekly:
            current_time = each.start_time
            while current_time <= each.weekly or (
                current_time.year == each.weekly.year
                and current_time.month == each.weekly.month
                and current_time.day == each.weekly.day
            ):
                if are_two_times_conflicting(
                    start_time,
                    end_time,
                    current_time,
                    current_time + timedelta(minutes=each.duration),
                ):
                    return False
                current_time += timedelta(days=7)

        else:
            if are_two_times_conflicting(
                start_time,
                end_time,
                each.start_time,
                each.start_time + timedelta(minutes=each.duration),
            ):
                return False

    return True


def is_inside_rectangle(
    top_right_x: float,
    top_right_y: float,
    bottom_left_x: float,
    bottom_left_y: float,
    x: float,
    y: float,
) -> bool:
    return (
        x <= top_right_x
        and y <= top_right_y
        and x >= bottom_left_x
        and y >= bottom_left_y
    )
