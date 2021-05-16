from django.contrib.auth import logout as log_me_out
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View
from django.db.models import Q
from ascendo_web_page.rules.models import Rules
from .forms import ProfileForm
from .models import Profile


# Create your views here.
class ProfileView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                profile = user.profile
                return render(request, 'profile/start.html', {'rules': Rules.objects.all()})
            except Profile.DoesNotExist:
                form = ProfileForm(initial={'nick_name': user.username})
                return render(request, 'profile/profile.html', {'form': form})
        else:
            return redirect('home')

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            form = ProfileForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.last_submission = now()
                form.save()
                return render(request, 'profile/start.html', {'rules': Rules.objects.all()})
        else:
            return redirect('home')


profile_view = ProfileView.as_view()


class LeaderView(View):
    def get(self, request):
        context = {'profiles': Profile.objects.filter(Q(code=True) | Q(language=True))}
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile:
                    if profile.language:
                        context['text'] = "Let's Continue"
                        context['has_started'] = True
                    else:
                        context['text'] = "Let's Start"
                        context['has_started'] = False
            except Profile.DoesNotExist:
                context['text'] = "Let's Start"
                context['has_started'] = False
        else:
            context['text'] = "Let's Start"
            context['has_started'] = False
        return render(request, 'profile/lead.html', context)


leader_view = LeaderView.as_view()


def logout(request):
    log_me_out(request)
    return redirect('home')
