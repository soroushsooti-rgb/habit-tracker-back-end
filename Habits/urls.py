
from django.urls import path
from . import views

urlpatterns = [

    path('habits/', views.HabitView.as_view(), name='habit'),



]
