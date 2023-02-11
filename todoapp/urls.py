from django.urls import path 

from . import views 

urlpatterns = [
    path('todo/', views.GetAllTodo.as_view(), name='getAll'),
    path('todo/<int:pk>/', views.OneTodo.as_view(), name='oneTodo')
]

