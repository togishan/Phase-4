from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(
        User, related_name="organizations", on_delete=models.CASCADE
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner.to_dict(),
        }


class UserPermissionForOrganization(models.Model):
    user = models.ManyToManyField(User, related_name="organization_permissions")
    organization = models.ManyToManyField(Organization, "permissions")
    permission = models.CharField(
        max_length=256,
        choices=(
            ("LIST", "LIST"),
            ("ADD", "ADD"),
            ("ACCESS", "ACCESS"),
            ("DELETE", "DELETE"),
        ),
    )


class Room(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name="rooms", on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    capacity = models.IntegerField()

    organization = models.ForeignKey(
        Organization, related_name="rooms", on_delete=models.CASCADE
    )  # Added field

    # Format HH:MM which denotes the time the room opens in 24 hour format (e.g. 13:00)
    open_time = models.CharField(max_length=256)
    close_time = models.CharField(max_length=256)

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


class UserPermissionForRoom(models.Model):
    user = models.ManyToManyField(User, related_name="room_permissions")
    room = models.ManyToManyField(Room, related_name="permissions")
    permission = models.CharField(
        max_length=256,
        choices=(
            ("WRITE", "WRITE"),
            ("LIST", "LIST"),
            ("RESERVE", "RESERVE"),
            ("PERRESERVE", "PERRESERVE"),
            ("DELETE", "DELETE"),
        ),
    )


class Event(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    category = models.CharField(
        max_length=256,
        choices=(
            ("MEETING", "MEETING"),
            ("LECTURE", "LECTURE"),
            ("CONCERT", "CONCERT"),
            ("SEMINAR", "SEMINAR"),
            ("STUDY", "STUDY"),
        ),
    )
    capacity = models.IntegerField()
    duration = models.IntegerField()
    start_time = models.TimeField(null=True)
    location = models.ForeignKey(
        Room, related_name="events", null=True, on_delete=models.SET_NULL, blank = True
    )
    weekly = models.DateTimeField(null=True, blank = True)

    def to_dict(self):
        from .dependency_manager import DependencyManager

        user: User = DependencyManager.get(User)

        try:
            if user.id != self.owner.id:
                UserPermissionForEvent.get(
                    (UserPermissionForEvent.user_id == user.id)
                    & (UserPermissionForEvent.event_id == self.id)
                    & (UserPermissionForEvent.permission == "READ")
                )

            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "owner": self.owner.to_dict(),
                "category": self.category,
                "capacity": self.capacity,
                "duration": self.duration,
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "location": self.location.to_dict() if self.location else None,
                "weekly": self.weekly,
            }

        except:
            return {"title": "No permission to view this event"}


class UserPermissionForEvent(models.Model):
    user = models.ManyToManyField(User, related_name="event_permissions")
    event = models.ManyToManyField(Event, related_name="permissions")
    permission = models.CharField(
        max_length=256,
        choices=(
            ("WRITE", "WRITE"),
            ("READ", "READ"),
        ),
    )
