from django.shortcuts import get_object_or_404, redirect, render
from .forms import CourseForm, LessonForm
from .models import Courses, Lessons, Questions, TestResults, Tests, UserCourses, Users


# 1. Список усіх курсів
def courses_list(request):
    courses = Courses.objects.all().order_by('-create_at')
    return render(
        request, 'learniva_app/courses_list.html', {'courses': courses}
    )


# 2. Деталі курсу зі списком уроків
def course_detail(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    lessons = Lessons.objects.filter(courses_course=course).order_by('order_number')
    return render(
        request,
        'learniva_app/course_detail.html',
        {'course': course, 'lessons': lessons},
    )


# 3. Перегляд окремого уроку та пов'язаних тестів
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)
    tests = Tests.objects.filter(lessons_lessons=lesson)
    return render(
        request,
        'learniva_app/lesson_detail.html',
        {'lesson': lesson, 'tests': tests},
    )


# 4. Проходження тесту та перевірка відповідей
def test_detail(request, test_id):
    test = get_object_or_404(Tests, pk=test_id)
    questions = Questions.objects.filter(tests_test=test).order_by('order_number')

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        results_detail = []

        for question in questions:
            selected_answer = request.POST.get(f'question_{question.question_id}')
            is_correct = selected_answer == question.correct_answer
            if is_correct:
                score += 1

            results_detail.append({
                'question': question.question_text,
                'selected': selected_answer,
                'correct': question.correct_answer,
                'is_correct': is_correct,
            })

        default_user = Users.objects.first()
        if default_user:
            TestResults.objects.create(
                score=score, users_user=default_user, tests_test=test
            )

        return render(
            request,
            'learniva_app/test_result.html',
            {
                'test': test,
                'score': score,
                'total_questions': total_questions,
                'results_detail': results_detail,
            },
        )

    return render(
        request,
        'learniva_app/test_detail.html',
        {
            'test': test,
            'questions': questions,
        },
    )


# 5. Створення нового курсу
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm()
    return render(request, 'learniva_app/course_form.html', {'form': form})


# 6. Видалення курсу
def course_delete(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_list')
    return render(
        request, 'learniva_app/course_confirm_delete.html', {'course': course}
    )


# 7. Додавання уроку до курсу
def add_lesson(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.courses_course = course
            lesson.save()
            return redirect('course_detail', course_id=course.course_id)
    else:
        form = LessonForm()

    return render(
        request,
        'learniva_app/add_lesson.html',
        {'form': form, 'course': course},
    )


# 8. Редагування уроку
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_detail', lesson_id=lesson.lessons_id)
    else:
        form = LessonForm(instance=lesson)
    return render(
        request,
        'learniva_app/edit_lesson.html',
        {'form': form, 'lesson': lesson},
    )


# 9. Видалення уроку
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)
    course_id = lesson.courses_course.course_id
    if request.method == 'POST':
        lesson.delete()
        return redirect('course_detail', course_id=course_id)
    return render(
        request, 'learniva_app/delete_lesson.html', {'lesson': lesson}
    )