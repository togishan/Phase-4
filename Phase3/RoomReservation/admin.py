from django.contrib import admin

# Register your models here.
from RoomReservation.models import Organization, UserPermissionForOrganization, Room, UserPermissionForRoom, RoomInOrganization, Event, UserPermissionForEvent

admin.site.register(Organization)
admin.site.register(UserPermissionForOrganization)
admin.site.register(Room)
admin.site.register(UserPermissionForRoom)
admin.site.register(RoomInOrganization)
admin.site.register(Event)
admin.site.register(UserPermissionForEvent)