from django.urls import path, include
from . import views
from .views import (
    main_page,
    organization_list,
    create_organization,
    update_organization,
    delete_organization,
)

urlpatterns = [
    path("", main_page, name="main_page"),
    # path("", views.index, name="index"),
    path("accounts/register/", views.RegistrationView.as_view(), name="registration"),
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
]
