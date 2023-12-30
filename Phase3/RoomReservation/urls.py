from django.urls import path
from .views import (
    main_page,
    organization_list,
    create_organization,
    update_organization,
    delete_organization,
)

from .views import room_list, create_room, update_room, delete_room


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
]
