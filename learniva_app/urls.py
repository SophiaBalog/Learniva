from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='courses_list', permanent=False)),

    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/add-lesson/', views.add_lesson, name='add_lesson'),

    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('lessons/<int:lesson_id>/add-test/', views.add_test, name='add_test'),

    path('tests/<int:test_id>/', views.test_detail, name='test_detail'),
    path('tests/<int:test_id>/add-question/', views.add_question, name='add_question'),
    path('my-results/', views.my_results, name='my_results'),
    
    path('signup/', views.signup, name='signup'),
]