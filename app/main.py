from .auth.User import User
from .auth.UserGroup import UserGroup
from .library.Organization import Organization
from .library.Event import Event, EventCategory
from .library.Room import Room
from .library.HourMinute import HourMinute
from .dependency_manager import DependencyManager
from datetime import datetime
from .library.Rectangle import Rectangle


# test reserve method to check it reserves event properly and 
# on encountering with conflict discarding and returning False
def test0():
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
    keynote_event5 = Event(
        title="Keynote3",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=800,
    )
    print(google_organization.reserve(
        event=keynote_event1,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 8, 8, 0),
    ))
    # try to add event which occupies main room in dates:
    #   (y:2023, m:1, d:1, h:8)
    #   (y:2023, m:1, d:8, h:8)
    #   (y:2023, m:1, d:15, h:8)
    #   (y:2023, m:1, d:22, h:8)
    # WILL FAIL: clashes with keynote_event1
    print(google_organization.reserve(
        event=keynote_event2,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 1, 8, 0),
    ))
    # try to add event which occupies main room in dates:
    #   (y:2023, m:1, d:15, h:9)
    #   (y:2023, m:1, d:22, h:9)
    #   (y:2023, m:1, d:29, h:9)
    # WILL SUCCESS
    print(google_organization.reserve(
        event=keynote_event3,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 15, 9, 0),
    ))
    # try to add event which occupies main room in dates:
    #   (y:2022, m:12, d:25, h:9)
    #   (y:2023, m:1, d:1, h:9)
    #   (y:2023, m:1, d:8, h:9)
    #   (y:2023, m:1, d:15, h:9)
    # WILL FAIL: clashes with keynote_event3
    print(google_organization.reserve(
        event=keynote_event4,
        room_id=main_room.id,
        start_time=datetime(2022, 12, 25, 9, 0),
    ))
    # try to add same but shifting time by 30 mins before 9:00
    # WILL FAIL: the event will take an hour. The event that starts
    # at 8:30 will end in 9:30 and will clash with the event between 8:00 and 9:00

    print(google_organization.reserve(
        event=keynote_event4,
        room_id=main_room.id,
        start_time=datetime(2022, 12, 25, 8, 30),
    ))
    # try to add an event which exceeds the closing time
    print(google_organization.reserve(
        event=keynote_event5,
        room_id=main_room.id,
        start_time=datetime(2024, 1, 1, 9, 00),
    ))
    print(google_organization.get())

# test find_room function
def test1():
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
        duration=120,
        weekly=datetime(2023,2,15)
    )
    keynote_event2 = Event(
        title="Keynote2",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=180,
        weekly=datetime(2023,2,25)
    )
    keynote_event3 = Event(
        title="Keynote3",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=800,
    )
    # reserve the dates
    # 2023-01-22 10:00  
    # 2023-01-29 10:00
    # for keynote_event1
    google_organization.reserve(
        event=keynote_event1,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 22, 10, 0),
    )
    # find available hours for rooms
    # 2023-01-22 11:00 will be discarded since the event will 
    # conflict with keynote_event1 which takes place hours between 10:00-12:00 
    lst = google_organization.find_room(keynote_event2, Rectangle(0,0,5,5), datetime(2023,1,21),datetime(2023,1,23), 180)
    for i in lst:
        print(i[2])
    print("###")
    # 2023-01-29 09:00 
    # 2023-01-29 10:00
    # 2023-01-29 11:00
    # will be discarded, since the event that starts these hours and takes 2 hours will conflict
    # with weekly keynote_event1 which takes place between 2023-01-29 10:00 and 2023-01-29 12:00
    # Also
    # 2023-02-05 09:00 
    # 2023-02-05 10:00
    # 2023-02-05 11:00
    # will also conflict with keynote_event1 so they will be discarded too
    lst = google_organization.find_room(keynote_event2, Rectangle(0,0,5,5), datetime(2023,1,29),datetime(2023,2,7), 60)
    for i in lst:
        print(i[2])
    print("###")
    # try to find a reservation for an event which exceeds room's working hours
    lst = google_organization.find_room(keynote_event3, Rectangle(0,0,5,5), datetime(2023,1,29),datetime(2023,2,7), 60)
    for i in lst:
        print(i[2])
# test for checking operator overloading for Event class and observe 
# Python list.sort() function works as desired 
def test2():
    ev1 = Event(
        title="Keynote",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=60,
    )
    ev2 = Event(
        title="Keynote2",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=80,
    )
    ev3 =  Event(
        title="Keynote3",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=70,
    )
    ev4 =  Event(
        title="Keynote4",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=70,
    )
    lst = [ev1,ev2,ev3,ev4]
    lst.sort(reverse=True)
    for i in lst:
        print(i.get())


# test whether find_schedule works as intended
def test3():
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
    ev1 = Event(
        title="Keynote",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=60,
        weekly=datetime(2023,3,8),
    )
    ev2 = Event(
        title="Keynote2",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=80,
    )
    ev3 =  Event(
        title="Keynote3",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=70,
    )
    ev4 =  Event(
        title="Keynote4",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=70,
    )
    ev5 =  Event(
        title="Keynote5",
        description="Keynote by Google Developers Club",
        category=EventCategory.CONCERT,
        capacity=100,
        duration=800,
    )
    google_organization.reserve(
        event = ev1,
        room_id=main_room.id,
        start_time=datetime(2023, 1, 22, 10, 0),
    )
    lst = [ev2,ev3,ev4]
    lst2 = google_organization.find_schedule(lst, Rectangle(0,0,5,5), datetime(2023,1,29),datetime(2023,1,31), 60)
    for i in lst2:
        print(i[0].get(), i[2])
    print("###")

    # try to find schedule with an event which exceeds working hours
    lst = [ev2,ev3,ev4,ev5]
    lst2 = google_organization.find_schedule(lst, Rectangle(0,0,5,5), datetime(2023,1,29),datetime(2023,1,31), 60)
    for i in lst2:
        print(i[0].get(), i[2])
def main():
    test0()
    test1()
    test2()
    test3()

if __name__ == "__main__":
    main()