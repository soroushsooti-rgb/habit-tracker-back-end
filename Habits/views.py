from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Habit, HabitCheck
from .serializers import Habitserializers, HabitCheckSerializers


class HabitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        habits = Habit.objects.filter(user=request.user)
        serializer = Habitserializers(habits, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Habitserializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChekingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        checks = HabitCheck.objects.filter(habit__user=request.user)
        serializer = HabitCheckSerializers(checks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HabitCheckSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
