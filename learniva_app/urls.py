from django.urls import path
from . import views

urlpatterns = [
    # Маршрут для списку курсів
    path('courses/', views.courses_list, name='courses_list'),
]