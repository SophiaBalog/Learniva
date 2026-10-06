from django.shortcuts import get_object_or_404, redirect, render
from .forms import CourseForm, LessonForm, TestForm, QuestionForm
from .models import Courses, Lessons, Questions, TestResults, Tests, UserCourses, Users


def courses_list(request):
    courses = Courses.objects.all().order_by('-create_at')
    return render(
        request, 'learniva_app/courses_list.html', {'courses': courses}
    )


def course_detail(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    lessons = Lessons.objects.filter(courses_course=course).order_by('order_number')
    return render(
        request,
        'learniva_app/course_detail.html',
        {'course': course, 'lessons': lessons},
    )


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)
    tests = Tests.objects.filter(lessons_lessons=lesson)
    return render(
        request,
        'learniva_app/lesson_detail.html',
        {'lesson': lesson, 'tests': tests},
    )


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


def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm()
    return render(request, 'learniva_app/course_form.html', {'form': form})


def course_delete(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_list')
    return render(
        request, 'learniva_app/course_confirm_delete.html', {'course': course}
    )


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


def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)
    course_id = lesson.courses_course.course_id
    if request.method == 'POST':
        lesson.delete()
        return redirect('course_detail', course_id=course_id)
    return render(
        request, 'learniva_app/delete_lesson.html', {'lesson': lesson}
    )


def add_test(request, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)
    form = TestForm(request.POST or None)
    if form.is_valid():
        test = form.save(commit=False)
        test.lessons_lessons = lesson
        test.save()
        return redirect('add_question', test_id=test.test_id)
    return render(request, 'learniva_app/add_test.html', {'form': form, 'lesson': lesson})


def add_question(request, test_id):
    test = get_object_or_404(Tests, pk=test_id)
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.tests_test = test
        question.save()
        # Кнопка "Додати ще питання" повертає на цю ж сторінку
        if 'add_more' in request.POST:
            return redirect('add_question', test_id=test.test_id)
        return redirect('lesson_detail', lesson_id=test.lessons_lessons_id)
    return render(request, 'learniva_app/add_question.html', {'form': form, 'test': test})