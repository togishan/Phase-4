# forms.py
from django import forms
from .models import (
    Organization,
    Room,
    Event,
    UserPermissionForOrganization,
    UserPermissionForRoom,
    UserPermissionForEvent,
)


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "owner"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            "name",
            "owner",
            "organization",
            "x",
            "y",
            "capacity",
            "open_time",
            "close_time",
        ]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "owner",
            "category",
            "capacity",
            "duration",
            "start_time",
            "location",
            "weekly",
        ]


class UserPermissionForOrganizationForm(forms.ModelForm):
    class Meta:
        model = UserPermissionForOrganization
        fields = ["user", "organization", "permission"]


class UserPermissionForRoomForm(forms.ModelForm):
    class Meta:
        model = UserPermissionForRoom
        fields = ["user", "room", "permission"]


class UserPermissionForEventForm(forms.ModelForm):
    class Meta:
        model = UserPermissionForEvent
        fields = ["user", "event", "permission"]
