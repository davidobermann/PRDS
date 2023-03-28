from django.db.models import Sum, F, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
import datetime

from app.models import Journey, Goal


class GoalProgressEntry:
    def __init__(self, goal, progress):
        self.goal = goal
        self.progress = progress


def get_main_goal(user):
    maingoal = Goal.objects.filter(user=user, is_main=True).values()
    if not maingoal:
        return None
    else:
        return maingoal


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

def on_journey_delete(user, journey):
    goals_affected = Goal.objects.filter(
        user=user,
        startdate__lte=journey.date,
        enddate__gte=journey.date).all()

    for goal in goals_affected:
        if goal.type == 'FQ':
            goal.progress -= 1
        else:
            goal.progress -= journey.price
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
    ayearago = timezone.now().date() + datetime.timedelta(days=(-365))
    query = Journey.objects.filter(user=user, date__range=[ayearago, now])
    result = query.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('timestamp')).all()
    monthcnt = [0] * 12
    for item in result:
        monthcnt[item['month'].month-1] = item['total']
    return monthcnt


def get_dashboard_data_total(user):
    all_travels = Journey.objects.filter(user=user).count()
    goals_reached = Goal.objects.filter(user=user, progress__gte=F('criteria')).count()
    money_traveld = Journey.objects.filter(user=user).aggregate(Sum('price'))['price__sum'] or 0
    return all_travels, goals_reached, money_traveld


def get_dashboard_data_last365(user):
    now = timezone.now().date()
    ayearago = timezone.now().date() + datetime.timedelta(days=-365)
    all_travels = Journey.objects.filter(user=user, date__range=(ayearago, now)).count()
    goals_reached = Goal.objects.filter(user=user, progress__gte=F('criteria')).count()
    money_traveld = Journey.objects.filter(user=user).aggregate(Sum('price'))['price__sum'] or 0
    return all_travels, goals_reached, money_traveld

def get_money_last_12_months(user):
    now = timezone.now().date()
    ayearago = timezone.now().date() + datetime.timedelta(days=(-365))
    query = Journey.objects.filter(user=user, date__range=[ayearago, now])
    result = query.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('price')).all()
    monthcnt = [0] * 12
    for item in result:
        monthcnt[item['month'].month - 1] = item['total']
    return monthcnt

def get_price_plot_last365(user):
    now = timezone.now().date()
    ayearago = timezone.now().date() + datetime.timedelta(days=-365)
    prices = Journey.objects.filter(user=user, date__range=(ayearago, now)).values('price')
    return prices