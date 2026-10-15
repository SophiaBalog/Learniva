from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import CourseForm, LessonForm, QuestionForm, TestForm
from .models import Courses, Lessons, Questions, TestResults, Tests
from .permissions import teacher_required


class TeacherRequiredMixin:
    @method_decorator(teacher_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CourseListView(ListView):
    model = Courses
    template_name = 'learniva_app/courses_list.html'
    context_object_name = 'courses'
    ordering = ['-create_at']


class CourseDetailView(DetailView):
    model = Courses
    pk_url_kwarg = 'course_id'
    template_name = 'learniva_app/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = (Lessons.objects
                              .filter(courses_course=self.object)
                              .order_by('order_number'))
        return context


class CourseCreateView(TeacherRequiredMixin, CreateView):
    form_class = CourseForm
    template_name = 'learniva_app/course_form.html'
    success_url = reverse_lazy('courses_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Курс «{self.object.title}» створено.')
        return response


class CourseUpdateView(TeacherRequiredMixin, UpdateView):
    model = Courses
    form_class = CourseForm
    pk_url_kwarg = 'course_id'
    template_name = 'learniva_app/course_form.html'

    def get_success_url(self):
        return reverse('course_detail', kwargs={'course_id': self.object.course_id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Курс «{self.object.title}» оновлено.')
        return response


class CourseDeleteView(TeacherRequiredMixin, DeleteView):
    model = Courses
    pk_url_kwarg = 'course_id'
    template_name = 'learniva_app/course_confirm_delete.html'
    context_object_name = 'course'
    success_url = reverse_lazy('courses_list')

    def form_valid(self, form): 
        title = self.object.title
        response = super().form_valid(form)
        messages.success(self.request, f'Курс «{title}» видалено.')
        return response


class LessonDetailView(DetailView):
    model = Lessons
    pk_url_kwarg = 'lesson_id'
    template_name = 'learniva_app/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = (Tests.objects
                            .filter(lessons_lessons=self.object)
                            .annotate(q_count=Count('questions')))
        return context


class LessonCreateView(TeacherRequiredMixin, CreateView):
    form_class = LessonForm
    template_name = 'learniva_app/add_lesson.html'

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Courses, pk=kwargs['course_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

    def form_valid(self, form):
        form.instance.courses_course = self.course
        response = super().form_valid(form)
        messages.success(self.request, f'Урок «{self.object.title}» додано.')
        return response

    def get_success_url(self):
        return reverse('course_detail', kwargs={'course_id': self.course.course_id})


class LessonUpdateView(TeacherRequiredMixin, UpdateView):
    model = Lessons
    form_class = LessonForm
    pk_url_kwarg = 'lesson_id'
    template_name = 'learniva_app/edit_lesson.html'
    context_object_name = 'lesson'

    def get_success_url(self):
        return reverse('lesson_detail', kwargs={'lesson_id': self.object.lessons_id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Урок оновлено.')
        return response


class LessonDeleteView(TeacherRequiredMixin, DeleteView):
    model = Lessons
    pk_url_kwarg = 'lesson_id'
    template_name = 'learniva_app/delete_lesson.html'
    context_object_name = 'lesson'

    def get_success_url(self):
        return reverse('course_detail',
                       kwargs={'course_id': self.object.courses_course.course_id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Урок видалено.')
        return response


class TestCreateView(TeacherRequiredMixin, CreateView):
    form_class = TestForm
    template_name = 'learniva_app/add_test.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lessons, pk=kwargs['lesson_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.lesson
        return context

    def form_valid(self, form):
        form.instance.lessons_lessons = self.lesson
        response = super().form_valid(form)
        messages.success(self.request, 'Тест створено. Тепер додайте питання.')
        return response

    def get_success_url(self):
        return reverse('add_question', kwargs={'test_id': self.object.test_id})


class QuestionCreateView(TeacherRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'learniva_app/add_question.html'

    def dispatch(self, request, *args, **kwargs):
        self.test = get_object_or_404(Tests, pk=kwargs['test_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.test
        return context

    def form_valid(self, form):
        form.instance.tests_test = self.test
        response = super().form_valid(form)
        messages.success(self.request, 'Питання додано.')
        return response

    def get_success_url(self):
        if 'add_more' in self.request.POST:
            return reverse('add_question', kwargs={'test_id': self.test.test_id})
        return reverse('lesson_detail',
                       kwargs={'lesson_id': self.test.lessons_lessons_id})


class TestDetailView(LoginRequiredMixin, View):

    def get_objects(self, test_id):
        test = get_object_or_404(Tests, pk=test_id)
        questions = Questions.objects.filter(tests_test=test).order_by('order_number')
        return test, questions

    def get(self, request, test_id):
        test, questions = self.get_objects(test_id)
        return render(request, 'learniva_app/test_detail.html',
                      {'test': test, 'questions': questions})

    def post(self, request, test_id):
        test, questions = self.get_objects(test_id)
        score = 0
        results_detail = []

        for question in questions:
            selected = request.POST.get(f'question_{question.question_id}')
            is_correct = selected == question.correct_answer
            score += is_correct
            results_detail.append({
                'question': question.question_text,
                'selected': selected,
                'correct': question.correct_answer,
                'is_correct': is_correct,
            })

        TestResults.objects.create(score=score, user=request.user, test=test)
        return render(request, 'learniva_app/test_result.html', {
            'test': test,
            'score': score,
            'total_questions': questions.count(),
            'results_detail': results_detail,
        })


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('courses_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Реєстрація пройшла успішно. Ласкаво просимо!')
        return response


class MyResultsView(LoginRequiredMixin, ListView):
    template_name = 'learniva_app/my_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        return (TestResults.objects
                .filter(user=self.request.user)
                .select_related('test')
                .order_by('-complete_at'))