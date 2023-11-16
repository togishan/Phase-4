from .library.Event import Event, EventCategory
from .library.Room import Room
from .library.HourMinute import HourMinute


def main():
    main_room = Room(
        name="Main Room",
        x=1,
        y=2,
        capacity=10,
        open_time=HourMinute(8, 0),
        close_time=HourMinute(17, 0),
        permissions=[],
    )

    keynote_event = Event(
        title="Keynote",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        category=EventCategory.CONCERT,
        capacity=10,
        duration=10,
        permissions=[],
    )

    print(keynote_event.get())
    print(main_room.get())


if __name__ == "__main__":
    main()
