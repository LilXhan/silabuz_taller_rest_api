from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Todo
from .serializers import TodoSerializer

class GetAllTodo(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Todo.objects.all()
        serializer = TodoSerializer(tasks, many=True)

        return Response({
            'ok': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        Todo.objects.all().delete()

        return Response({
            'ok': True,
            'message': 'All Todo Deleted'
        }, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'ok': True,
                'message': 'Todo created'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'ok': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class OneTodo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(task)

        return Response({
            'ok': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = get_object_or_404(Todo, pk=pk)

        serializer = TodoSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'ok': True,
                'message': 'Todo updated'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'ok': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, resquest, pk):
        task = get_object_or_404(Todo, pk=pk)
        task.delete()
        return Response({
            'ok': True,
            'message': 'Todo deleted'
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        task = get_object_or_404(Todo, pk=pk)

        serializer = TodoSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'ok': True,
                'message': 'Todo updated'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'ok': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)