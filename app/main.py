from .auth.User import User
from .auth.UserGroup import UserGroup
from .library.Organization import Organization
from .library.Event import Event, EventCategory
from .library.Room import Room
from .library.HourMinute import HourMinute
from .dependency_manager import DependencyManager
from datetime import datetime


def main():
    organizer = User(name="John Doe", user_groups=[])
    DependencyManager.register(User, organizer)

    main_room = Room(
        name="Main Room",
        x=1,
        y=1,
        capacity=100,
        open_time=HourMinute(8, 0),
        close_time=HourMinute(17, 0),
        user_groups=[UserGroup.ADMIN],
    )

    google_organization = Organization(
        name="Google Developers Club",
        owner=organizer,
        rooms={main_room},
    )
    DependencyManager.register(Organization, google_organization)

    keynote_event = Event(
        title="Keynote",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=60,
    )

    print(organizer.get())
    print(google_organization.get())
    print(keynote_event.get())

    google_organization.reserve(
        event=keynote_event,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 1, 8, 0),
    )

    print(google_organization.get())


if __name__ == "__main__":
    main()
