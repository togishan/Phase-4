from .auth.User import User
from .auth.UserGroup import UserGroup
from .library.Organization import Organization
from .library.Event import Event, EventCategory
from .library.Room import Room
from .library.HourMinute import HourMinute
from .dependency_manager import DependencyManager
from datetime import datetime
from .library.Rectangle import Rectangle

def test():
    organizer = User(name="John Doe", user_groups=[])
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
        map=Rectangle(
            bottom_left_x=0,
            bottom_left_y=0,
            top_right_x=100,
            top_right_y=100,
        ),
        rooms={main_room},
    )
    
    keynote_event1 = Event(
        title="Keynote1",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=60,
    )
    keynote_event2 = Event(
        title="Keynote2",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=60,
        weekly=datetime(2023,1,22),
    )
    keynote_event3 = Event(
        title="Keynote3",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=60,
        weekly=datetime(2023,1,29),
    )
    keynote_event4 = Event(
        title="Keynote4",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=60,
        weekly=datetime(2023,1,15),
    )
    google_organization.reserve(
        event=keynote_event1,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 8, 8, 0),
    )
    # try to add event which occupies main room in dates:
    #   (y:2023, m:1, d:1, h:8)
    #   (y:2023, m:1, d:8, h:8)
    #   (y:2023, m:1, d:15, h:8)
    #   (y:2023, m:1, d:22, h:8)
    # WILL FAIL: clashes with keynote_event1
    google_organization.reserve(
        event=keynote_event2,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 1, 8, 0),
    )
    # try to add event which occupies main room in dates:
    #   (y:2023, m:1, d:15, h:9)
    #   (y:2023, m:1, d:22, h:9)
    #   (y:2023, m:1, d:29, h:9)
    # WILL SUCCESS
    google_organization.reserve(
        event=keynote_event3,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 15, 9, 0),
    )
    # try to add event which occupies main room in dates:
    #   (y:2022, m:12, d:25, h:9)
    #   (y:2023, m:1, d:1, h:9)
    #   (y:2023, m:1, d:8, h:9)
    #   (y:2023, m:1, d:15, h:9)
    # WILL FAIL: clashes with keynote_event3
    google_organization.reserve(
        event=keynote_event4,
        room_id=main_room.id,
        start_time=datetime(2022, 12, 25, 10, 0),
    )
    print(google_organization.get())

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
        map=Rectangle(
            top_left_x=0,
            top_right_y=0,
            bottom_right_x=100,
            bottom_left_y=100,
        ),
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
    #main()
    test()