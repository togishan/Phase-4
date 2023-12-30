from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserCreationForm
    def get_success_url(self):
        return reverse_lazy('index')
	

@login_required
def index(request):

	user = User.objects.get(username = request.user)
      
	return render(request,'user.html', {'user':user})
