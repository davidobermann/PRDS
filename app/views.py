import os

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.utils import dateformat, timezone

from app.controller import *
from app.forms import JourneyForm, UploadFileForm, GoalForm
from app.models import Journey, Goal
from verzweiflung.settings import MEDIA_ROOT


# Create your views here.

def home(request):
    context = {}
    if request.user.is_authenticated:
        main_goal = get_main_goal(request.user)
        context['maingoal'] = main_goal
        context['progress'] = main_goal['progress'] / main_goal ['criteria']
        context['progress__'] = int(main_goal['progress'] / main_goal ['criteria'] * 100)
        context['is_fq'] = (main_goal['type'] == 'FQ')
    return render(request, 'app/index.html', context)  # dasisteingutespasswort

@login_required
def insights(request):
    #retrieve data for certain graphs and put data into context
    #render data in template
    context = {}
    #travels in the last 12 months:
    context['dash_board_data_total'] = get_dashboard_data_total(request.user)
    context['dash_board_data_last365'] = get_dashboard_data_last365(request.user)
    context['travels_last_12_months'] = get_travles_last_12_months(request.user)
    context['money_last_12_months'] = get_money_last_12_months(request.user)
    context['price_plot_last365'] = get_price_plot_last365(request.user)
    return render(request, 'app/insights.html', context)

@login_required
def set_main_goal(request, id):
    Goal.objects.filter(user=request.user).update(is_main=False)
    Goal.objects.filter(user=request.user, id=id).update(is_main=True)
    return redirect('see_goals')


@login_required
def addgoal(request):
    context = {}
    if request.method == 'GET':
        context['form'] = GoalForm()
        return render(request, 'app/addgoal.html', context)
    else:
        form = GoalForm(request.POST)
        if form.is_valid():
            user = request.user
            new = form.save(commit=False)
            new.user = user
            new.save()
            on_goal_insert(user, new)  # update the progress
            # for testing reasons
            # eval_goal_progress(user, new)
        else:
            print(form['startdate'].value())
            print(form.errors)
        return redirect('home')


@login_required
def see_data(request):
    data = get_journeys_for_user(request.user)
    context = {
        'journeys': data
    }
    return render(request, 'app/see_data.html', context)


@login_required
def see_goals(request):
    data = get_goals_for_user(request.user)
    context = {
        'goals': data
    }
    return render(request, 'app/see_goals.html', context)


def get_goals_for_user(user):
    return Goal.objects.filter(user=user).order_by('timestamp').values()


def get_journeys_for_user(user):
    return Journey.objects.filter(user=user).order_by('date').values()


@login_required
def addjourney(request):
    context = {}
    if request.method == 'GET':
        context['form'] = JourneyForm()
        return render(request, 'app/addjourney.html', context)
    else:
        form = JourneyForm(request.POST)
        if form.is_valid():
            print(form['date'].value())
            user = request.user
            new = form.save(commit=False)
            new.user = user
            new.save()
            on_journey_insert(user, new)  # update goal progress
        else:
            print(form['date'].value())
            print(form.errors)
        return redirect('home')


@login_required
def delete_journey(request, id):
    journey = Journey.objects.get(id=id)
    journey.delete()
    return redirect('see_data')

@login_required
def delete_goal(request, id):
    goal = Goal.objects.get(id=id)
    goal.delete()
    return redirect('see_goals')


def handle_uploaded_file(f, request):
    # find, save, read, delete file
    path = os.path.join(MEDIA_ROOT, f.name)

    # save file in chunks to disk
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # read file line by line and add it to the DB
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.split(';')
            data = {'origin': values[0],
                    'destination': values[1],
                    'price': values[2].replace(",", "."),
                    'date': values[3].replace("\r", "")}
            form = JourneyForm(data)
            if form.is_valid():
                user = request.user
                new = form.save(commit=False)
                new.user = user
                new.save()
                on_journey_insert(user, new)  # update progress of goals

    os.remove(path)


@login_required
def upload_journeys(request):
    context = {}
    if request.method == 'GET':
        form = UploadFileForm()
        context['form'] = UploadFileForm()
        return render(request, 'app/upload_journeys.html', context)
    else:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], request)
            return redirect('home')
        return redirect('home')
