from django.urls import path, include
from . import views

urlpatterns = [

    path('habits/', include([path("", views.HabitView.as_view(), name='habit-list'),
                            path('<int:pk>', views.HabitView.as_view(), name='habit-detail')])),




    path('checks/', include([path('', views.ChekingView.as_view(), name='checking-list'),
                            path('<int:pk>', views.ChekingView.as_view(), name='checking-detail')]))
]
