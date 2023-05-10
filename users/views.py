from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView
from .forms import ChangeGraspPowerForm
from .forms import SignUpForm
from .models import User

class UserView(DetailView):
    template_name = 'profile.html'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_data'] = {
            'email': user.email,
            'name': user.name,
            'grasp_power': user.grasp_power,
            'comprehension': user.comprehension,
            'engagement': user.engagement,
            'learning_speed': user.learning_speed,
            'curiosity': user.curiosity,
            'confidence': user.confidence,
        }
        return context


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('users:profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




def change_grasp_power_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = ChangeGraspPowerForm(request.POST)
        if form.is_valid():
            # retrieve the user instance with the given email
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            # update the grasp_power attribute
            user.grasp_power = form.cleaned_data['grasp_power']
            # save the changes to the database
            user.save()
            # redirect to a success page
            return redirect('success')
    else:
        # create a blank form
        form = ChangeGraspPowerForm()
    # render the template with the form
    return render(request, 'change_grasp_power.html', {'form': form})