from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import (
    Organization,
    Room,
    Event,
    UserPermissionForOrganization,
    UserPermissionForRoom,
    UserPermissionForEvent,
)
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from .forms import (
    OrganizationForm,
    RoomForm,
    EventForm,
    UserPermissionForOrganizationForm,
    UserPermissionForRoomForm,
    UserPermissionForEventForm,
)


# Create your views here.


class RegistrationView(CreateView):
    template_name = "registration/registration.html"
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy("main_page")


@login_required
def index(request):
    user = User.objects.get(username=request.user)

    return render(request, "user.html", {"user": user})


@login_required
def main_page(request):
    return render(request, "main_page.html")


@login_required
def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, "organization_list.html", {"organizations": organizations})


@login_required
def create_organization(request):
    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("organization_list")
    else:
        form = OrganizationForm()
    return render(request, "create_organization.html", {"form": form})


@login_required
def update_organization(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect("organization_list")
    else:
        form = OrganizationForm(instance=organization)
    return render(
        request,
        "update_organization.html",
        {"form": form, "organization": organization},
    )


@login_required
def delete_organization(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    organization.delete()
    return redirect("organization_list")


# ...


@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, "room_list.html", {"rooms": rooms})


@login_required
def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("room_list")
    else:
        form = RoomForm()
    return render(request, "create_room.html", {"form": form})


@login_required
def update_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("room_list")
    else:
        form = RoomForm(instance=room)
    return render(request, "update_room.html", {"form": form, "room": room})


@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect("room_list")


# Assume you already have views for the other models (Organization and Room)
# ...


@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, "event_list.html", {"events": events})


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "create_event.html", {"form": form})


@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "update_event.html", {"form": form, "event": event})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect("event_list")


# Assume you already have views for other models
# ...


@login_required
def user_permission_for_organization_list(request):
    permissions = UserPermissionForOrganization.objects.all()
    return render(
        request,
        "user_permission_for_organization_list.html",
        {"permissions": permissions},
    )


@login_required
def create_user_permission_for_organization(request):
    if request.method == "POST":
        form = UserPermissionForOrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_permission_for_organization_list")
    else:
        form = UserPermissionForOrganizationForm()
    return render(
        request, "create_user_permission_for_organization.html", {"form": form}
    )


@login_required
def update_user_permission_for_organization(request, permission_id):
    permission = get_object_or_404(UserPermissionForOrganization, id=permission_id)
    if request.method == "POST":
        form = UserPermissionForOrganizationForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            return redirect("user_permission_for_organization_list")
    else:
        form = UserPermissionForOrganizationForm(instance=permission)
    return render(
        request,
        "update_user_permission_for_organization.html",
        {"form": form, "permission": permission},
    )


@login_required
def delete_user_permission_for_organization(request, permission_id):
    permission = get_object_or_404(UserPermissionForOrganization, id=permission_id)
    permission.delete()
    return redirect("user_permission_for_organization_list")


# Assume you already have views for other models
# ...


@login_required
def user_permission_for_room_list(request):
    permissions = UserPermissionForRoom.objects.all()
    return render(
        request, "user_permission_for_room_list.html", {"permissions": permissions}
    )


@login_required
def create_user_permission_for_room(request):
    if request.method == "POST":
        form = UserPermissionForRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_permission_for_room_list")
    else:
        form = UserPermissionForRoomForm()
    return render(request, "create_user_permission_for_room.html", {"form": form})


@login_required
def update_user_permission_for_room(request, permission_id):
    permission = get_object_or_404(UserPermissionForRoom, id=permission_id)
    if request.method == "POST":
        form = UserPermissionForRoomForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            return redirect("user_permission_for_room_list")
    else:
        form = UserPermissionForRoomForm(instance=permission)
    return render(
        request,
        "update_user_permission_for_room.html",
        {"form": form, "permission": permission},
    )


@login_required
def delete_user_permission_for_room(request, permission_id):
    permission = get_object_or_404(UserPermissionForRoom, id=permission_id)
    permission.delete()
    return redirect("user_permission_for_room_list")


# Assume you already have views for other models
# ...


@login_required
def user_permission_for_event_list(request):
    permissions = UserPermissionForEvent.objects.all()
    return render(
        request, "user_permission_for_event_list.html", {"permissions": permissions}
    )


@login_required
def create_user_permission_for_event(request):
    if request.method == "POST":
        form = UserPermissionForEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_permission_for_event_list")
    else:
        form = UserPermissionForEventForm()
    return render(request, "create_user_permission_for_event.html", {"form": form})


@login_required
def update_user_permission_for_event(request, permission_id):
    permission = get_object_or_404(UserPermissionForEvent, id=permission_id)
    if request.method == "POST":
        form = UserPermissionForEventForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            return redirect("user_permission_for_event_list")
    else:
        form = UserPermissionForEventForm(instance=permission)
    return render(
        request,
        "update_user_permission_for_event.html",
        {"form": form, "permission": permission},
    )


@login_required
def delete_user_permission_for_event(request, permission_id):
    permission = get_object_or_404(UserPermissionForEvent, id=permission_id)
    permission.delete()
    return redirect("user_permission_for_event_list")
