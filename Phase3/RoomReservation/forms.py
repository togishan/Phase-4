# forms.py
from django import forms
from .models import Organization, Room, Event


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "owner"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "owner", "x", "y", "capacity", "open_time", "close_time"]


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
