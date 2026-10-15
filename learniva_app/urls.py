from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='courses_list'),
    path('courses/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:course_id>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:course_id>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('courses/<int:course_id>/lessons/add/', views.LessonCreateView.as_view(), name='add_lesson'),
    path('lessons/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:lesson_id>/edit/', views.LessonUpdateView.as_view(), name='edit_lesson'),
    path('lessons/<int:lesson_id>/delete/', views.LessonDeleteView.as_view(), name='delete_lesson'),
    path('lessons/<int:lesson_id>/tests/add/', views.TestCreateView.as_view(), name='add_test'),
    path('tests/<int:test_id>/', views.TestDetailView.as_view(), name='test_detail'),
    path('tests/<int:test_id>/questions/add/', views.QuestionCreateView.as_view(), name='add_question'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('my-results/', views.MyResultsView.as_view(), name='my_results'),
]