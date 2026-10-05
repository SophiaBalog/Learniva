from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path(
        'courses/<int:course_id>/', views.course_detail, name='course_detail'
    ),
    path(
        'courses/<int:course_id>/delete/',
        views.course_delete,
        name='course_delete',
    ),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('tests/<int:test_id>/', views.test_detail, name='test_detail'),
    path(
        'course/<int:course_id>/add-lesson/',
        views.add_lesson,
        name='add_lesson',
    ),
    path('tests/<int:test_id>/', views.test_detail, name='test_detail'),
]