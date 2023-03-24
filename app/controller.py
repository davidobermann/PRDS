from datetime import datetime

from django.db.models import Sum, F
from django.utils import timezone

from app.models import Journey, Goal


class GoalProgressEntry:
    def __init__(self, goal, progress):
        self.goal = goal
        self.progress = progress


def get_main_goal(user):
    maingoal = Goal.objects.filter(user=user, is_main=True).values()
    if maingoal.count() > 1:
        raise ValueError('Too many main goals specified')
    return maingoal[0]


def on_journey_insert(user, journey):
    goals_affected = Goal.objects.filter(
        user=user,
        startdate__lte=journey.date,
        enddate__gte=journey.date).all()

    for goal in goals_affected:
        if goal.type == 'FQ':
            goal.progress += 1
        else:
            goal.progress += journey.price
        goal.save(update_fields=['progress'])


def on_goal_insert(user, goal):
    goal.progress = eval_goal_progress(user, goal)
    goal.save(update_fields=['progress'])


def get_goals_with_progress_current(user):
    goalproglist = []
    goals = Goal.objects.filter(user=user).values()
    for goal in goals:
        progress = eval_goal_progress(user, goal)
        goalproglist.append(GoalProgressEntry(goal, progress))
    return goalproglist


def eval_goal_progress(user, goal):
    query = Journey.objects.filter(user=user, date__range=(goal.startdate, goal.enddate))

    if goal.type == 'FQ':
        price_sum = query.aggregate(Sum('price'))['price__sum']
        progress = price_sum / goal.criteria
        return progress
    else:
        count = query.count()
        progress = count / goal.criteria
        return progress


def get_travles_last_12_months(user):
    now = timezone.now().date()
    ayearago = timezone.now().date() + datetime.timedelta(days=-365)
    query = Journey.objects.filter(user=user, date__range=(now, ayearago))
    monthcnt = [None] * 12
    i = 0
    for month in monthcnt:
        monthcnt[i] = query.filter(date__month=i + 1).count()
        i += 1
    return monthcnt


def get_dashboard_data_total(user):
    all_travels = Journey.objects.filter(user=user).count()
    goals_reached = Goal.objects.filter(user=user, progress__gte=F('criteria')).count()
    money_traveld = Journey.objects.filter(user=user).aggregate(Sum('price'))
    return all_travels, goals_reached, money_traveld


def get_dashboard_data_last365(user):
    now = timezone.now().date()
    ayearago = timezone.now().date() + datetime.timedelta(days=-365)
    all_travels = Journey.objects.filter(user=user, date__range=(now, ayearago)).count()
    goals_reached = Goal.objects.filter(user=user, progress__gte=F('criteria')).count()
    money_traveld = Journey.objects.filter(user=user).aggregate(Sum('price'))

def get_money_last_12_months(user):
    now = timezone.now().date()
    ayearago = timezone.now().date() + datetime.timedelta(days=-365)
    query = Journey.objects.filter(user=user, date__range=(now, ayearago))
    monthcnt = [None] * 12
    i = 0
    for month in monthcnt:
        monthcnt[i] = query.filter(date__month=i + 1).aggregate(Sum('price'))
        i += 1
    return monthcnt

