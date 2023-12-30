# forms.py
from django import forms
from .models import Organization, Room


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "owner"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "owner", "x", "y", "capacity", "open_time", "close_time"]
