from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Organization
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from .forms import OrganizationForm

# Create your views here.


class RegistrationView(CreateView):
    template_name = "registration/registration.html"
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy("index")


@login_required
def index(request):
    user = User.objects.get(username=request.user)

    return render(request, "user.html", {"user": user})


def main_page(request):
    return render(request, "main_page.html")


def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, "organization_list.html", {"organizations": organizations})


def create_organization(request):
    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("organization_list")
    else:
        form = OrganizationForm()
    return render(request, "create_organization.html", {"form": form})


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


def delete_organization(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    organization.delete()
    return redirect("organization_list")
