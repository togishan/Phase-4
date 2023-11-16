from .library.User import User
from .library.Organization import Organization
from .library.Event import Event, EventCategory
from .library.Room import Room
from .library.HourMinute import HourMinute


def main():
    organizer = User()

    main_room = Room(
        name="Main Room",
        x=1,
        y=2,
        capacity=10,
        open_time=HourMinute(8, 0),
        close_time=HourMinute(17, 0),
        permissions=[],
    )

    google_organization = Organization(
        name="Google Developers Club",
        owner=organizer,
        rooms=[main_room],
    )

    keynote_event = Event(
        title="Keynote",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        category=EventCategory.CONCERT,
        capacity=10,
        duration=10,
        permissions=[],
    )

    print(google_organization.get())
    print(keynote_event.get())
    print(main_room.get())


if __name__ == "__main__":
    main()
