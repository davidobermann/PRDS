from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('addjourney', addjourney, name='addjourney'),
    path('delete_all', delete_all, name='delete_all'),
    path('upload_journeys', upload_journeys, name='upload_journeys'),
    path('see_data', see_data, name='see_data'),
    path('see_goals', see_goals, name='see_goals'),
    path('addgoal', addgoal, name='addgoal'),
    path('delete_journey/<int:id>', delete_journey, name='delete_journey'),
    path('delete_goal/<int:id>', delete_goal, name='delete_goal'),
    path('set_main_goal/<int:id>', set_main_goal, name='set_main_goal'),
    path('insights', insights, name='insights')
]
