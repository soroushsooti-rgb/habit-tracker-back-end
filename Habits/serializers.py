from rest_framework import serializers
from .models import Habit, HabitCheck


class Habitserializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'frequency',
                  'dat_of_week', 'day_of_month', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class HabitCheckSerializers (serializers.ModelSerializer):
    class Meta:
        model = HabitCheck
        fields = ['id', 'habit']
