from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Habit, HabitCheck
from .serializers import Habitserializers, HabitCheckSerializers


class HabitView (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            habit = Habit.objects.filter(pk=pk, user=request.user).first()
            if not habit:
                return Response("No specific habit was identified.")
            return Response(serializer.data)

        habits = Habit.objects.filter(user=request.user)
        serializer = Habitserializers(habits, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Habitserializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


    def  delete (self,request,pk):
        habit = Habit.objects.filter(pk=pk, user=request.user).first()
        habit.delete()
        return Response()
