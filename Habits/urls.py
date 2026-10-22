from django.urls import path
from . import views

urlpatterns = [

    path('habits/', views.HabitView.as_view(), name='habit-list'),
    path('habits/<int:pk>/', views.HabitView.as_view(), name='habit-detail'),


    path('checks/', views.ChekingView.as_view(), name='checking-list'),
    path('checks/<int:pk>/', views.ChekingView.as_view(), name='checking-detail'),
]
