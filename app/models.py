from peewee import *
from enum import Enum

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField(max_length=256)
    username = CharField(max_length=256, unique=True)
    password = CharField(max_length=256)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
        }


class Organization(BaseModel):
    name = CharField(max_length=256)
    owner = ForeignKeyField(User, backref="organizations")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner.to_dict(),
        }


class UserPermissionForOrganization(BaseModel):
    user = ForeignKeyField(User, backref="permissions")
    organization = ForeignKeyField(Organization, backref="permissions")
    permission = CharField(
        max_length=256,
        choices=(
            ("LIST", "LIST"),
            ("ADD", "ADD"),
            ("ACCESS", "ACCESS"),
            ("DELETE", "DELETE"),
        ),
    )


class Room(BaseModel):
    name = CharField(max_length=256)
    owner = ForeignKeyField(User, backref="rooms")
    x = DoubleField()
    y = DoubleField()
    capacity = IntegerField()

    # Format HH:MM which denotes the time the room opens in 24 hour format (e.g. 13:00)
    open_time = CharField(max_length=256)
    close_time = CharField(max_length=256)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner.to_dict(),
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity,
            "open_time": self.open_time,
            "close_time": self.close_time,
        }


class UserPermissionForRoom(BaseModel):
    user = ForeignKeyField(User, backref="permissions")
    room = ForeignKeyField(Room, backref="permissions")
    permission = CharField(
        max_length=256,
        choices=(("WRITE", "WRITE")),
    )


class RoomInOrganization(BaseModel):
    room = ForeignKeyField(Room, backref="organizations")
    organization = ForeignKeyField(Organization, backref="rooms")

    def to_dict(self):
        return {
            "room": self.room.to_dict(),
            "organization": self.organization.to_dict(),
        }


class Event(BaseModel):
    title = CharField(max_length=256)
    description = CharField(max_length=256)
    category = CharField(
        max_length=256,
        choices=(
            ("MEETING", "MEETING"),
            ("LECTURE", "LECTURE"),
            ("CONCERT", "CONCERT"),
            ("SEMINAR", "SEMINAR"),
            ("STUDY", "STUDY"),
        ),
    )
    capacity = IntegerField()
    duration = IntegerField()
    start_time = DateTimeField(null=True)
    location = ForeignKeyField(Room, backref="events", null=True)
    weekly = DateTimeField(null=True)


if __name__ == "__main__":
    # Create tables if they don't exist
    # This code will run when you run the models.py file directly
    db.connect()
    db.create_tables(
        [
            User,
            Organization,
            UserPermissionForOrganization,
            Room,
            UserPermissionForRoom,
            RoomInOrganization,
            Event,
        ]
    )
    db.close()
