from django.contrib.auth import login, authenticate
from django.http import Http404
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Activity
from .forms import NameForm, ActivityForm
from django.http import HttpResponseRedirect

def home_view(request):

    if request.user.is_authenticated and not hasattr(request.user, 'profile'):
        return redirect('/form')
    else: return render(request, 'home.html')

def form_view(request):

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.user.profile = Profile()
            request.user.profile.weight = form.cleaned_data['weight']
            request.user.profile.height=form.cleaned_data['height']
            request.user.profile.age=form.cleaned_data['age']
            request.user.profile.gender=form.cleaned_data['gender']
            request.user.profile.save()
            return redirect('/')
    else:
        form = NameForm()
    return render(request, 'login/form.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'login/signup.html', {'form': form})

def data_view(request):
    return render(request, 'login/data.html')

def update_view(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.user.profile.weight = form.cleaned_data['weight']
            request.user.profile.height=form.cleaned_data['height']
            request.user.profile.age=form.cleaned_data['age']
            request.user.profile.gender=form.cleaned_data['gender']
            request.user.profile.save()
            return redirect('data/')
    else:
        form = NameForm(initial={"weight":request.user.profile.weight, 'height':request.user.profile.height, 'age':request.user.profile.age, 'gender':request.user.profile.gender})
    return render(request, 'login/form.html', {'form': form})

def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            new_activity=Activity()
            new_activity.profile=request.user.profile
            new_activity.date=form.cleaned_data['date']
            new_activity.distance=form.cleaned_data['distance']
            new_activity.duration=form.cleaned_data['duration']
            new_activity.comment=form.cleaned_data['comment']
            new_activity.save()
            return redirect('/')
    else:
        form = ActivityForm()
    return render(request, 'login/form.html', {'form': form})

def history_view(request):
    history=Activity.objects.all().filter(profile=request.user.profile)
    contex = {'history':history}
    return render(request, 'login/history.html', contex)

def activity_detail_view(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.profile.id is not request.user.profile.id:
        raise Http404("Activity does not exist")
    calories = round(activity.distance*request.user.profile.weight*1.036)
    tempo = round(activity.duration/activity.distance, 2)
    return render(request, 'login/details.html', {'activity':activity, 'calories':calories, 'tempo': tempo})

def remove_view(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.profile.id is not request.user.profile.id:
        raise Http404("Activity does not exist")
    activity.delete()
    return render(request, 'login/deleted.html')

def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.profile.id is not request.user.profile.id:
        raise Http404("Activity does not exist")
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity.date=form.cleaned_data['date']
            activity.distance=form.cleaned_data['distance']
            activity.duration=form.cleaned_data['duration']
            activity.comment=form.cleaned_data['comment']
            activity.save()
            return redirect('/view_history')
    else:
        form = ActivityForm(initial={'date':activity.date, 'distance':activity.distance, 'duration':activity.duration, 'comment':activity.comment})
    return render(request, 'login/form.html', {'form': form})