from django.urls import path
from .views import (
    main_page,
    organization_list,
    create_organization,
    update_organization,
    delete_organization,
)

from .views import room_list, create_room, update_room, delete_room
from .views import event_list, create_event, update_event, delete_event
from .views import (
    user_permission_for_organization_list,
    create_user_permission_for_organization,
    update_user_permission_for_organization,
    delete_user_permission_for_organization,
)
from .views import (
    user_permission_for_room_list,
    create_user_permission_for_room,
    update_user_permission_for_room,
    delete_user_permission_for_room,
)


urlpatterns = [
    path("", main_page, name="main_page"),
    # Organization URLs
    path("organizations/", organization_list, name="organization_list"),
    path("organizations/create/", create_organization, name="create_organization"),
    path(
        "organizations/<int:organization_id>/update/",
        update_organization,
        name="update_organization",
    ),
    path(
        "organizations/<int:organization_id>/delete/",
        delete_organization,
        name="delete_organization",
    ),
    # Room URLs
    path("rooms/", room_list, name="room_list"),
    path("rooms/create/", create_room, name="create_room"),
    path("rooms/<int:room_id>/update/", update_room, name="update_room"),
    path("rooms/<int:room_id>/delete/", delete_room, name="delete_room"),
    # Event URLs
    path("events/", event_list, name="event_list"),
    path("events/create/", create_event, name="create_event"),
    path("events/<int:event_id>/update/", update_event, name="update_event"),
    path("events/<int:event_id>/delete/", delete_event, name="delete_event"),
    # User Permission for Organization URLs
    path(
        "user_permissions_for_organizations/",
        user_permission_for_organization_list,
        name="user_permission_for_organization_list",
    ),
    path(
        "user_permissions_for_organizations/create/",
        create_user_permission_for_organization,
        name="create_user_permission_for_organization",
    ),
    path(
        "user_permissions_for_organizations/<int:permission_id>/update/",
        update_user_permission_for_organization,
        name="update_user_permission_for_organization",
    ),
    path(
        "user_permissions_for_organizations/<int:permission_id>/delete/",
        delete_user_permission_for_organization,
        name="delete_user_permission_for_organization",
    ),
    # Add similar patterns for other models as needed
    # User Permission for Room URLs
    path(
        "user_permissions_for_rooms/",
        user_permission_for_room_list,
        name="user_permission_for_room_list",
    ),
    path(
        "user_permissions_for_rooms/create/",
        create_user_permission_for_room,
        name="create_user_permission_for_room",
    ),
    path(
        "user_permissions_for_rooms/<int:permission_id>/update/",
        update_user_permission_for_room,
        name="update_user_permission_for_room",
    ),
    path(
        "user_permissions_for_rooms/<int:permission_id>/delete/",
        delete_user_permission_for_room,
        name="delete_user_permission_for_room",
    ),
]
