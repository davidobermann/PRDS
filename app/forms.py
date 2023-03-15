import datetime

from django.utils import timezone, dateformat
from django import forms
from app.models import Journey, Goal


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))


class JourneyForm(forms.ModelForm):
    now = dateformat.format(timezone.now().date(), 'd.m.Y')
    #date = forms.DateField(initial=now, widget=forms.DateInput(attrs={'type': 'date'}), input_formats=["%d.%m.%Y"],)
    date = forms.DateField(input_formats=["%d.%m.%Y"], initial=now)

    class Meta:
        model = Journey
        fields = '__all__'
        exclude = ['user', 'timestamp']


class GoalForm(forms.ModelForm):
    now = dateformat.format(timezone.now().date(), 'd.m.Y')
    ayear = dateformat.format(timezone.now().date() + datetime.timedelta(days=365), 'd.m.Y')
    startdate = forms.DateField(input_formats=["%d.%m.%Y"], initial=now)
    enddate = forms.DateField(input_formats=["%d.%m.%Y"], initial=ayear)
    type = forms.ChoiceField(choices=Goal.GoalType.choices, widget=forms.RadioSelect())
    is_main = forms.BooleanField(label='This goal is the main goal to be displayed in the home screen.', required=False)

    class Meta:
        model = Goal
        fields = '__all__'
        exclude = ['user', 'timestamp', 'progress']