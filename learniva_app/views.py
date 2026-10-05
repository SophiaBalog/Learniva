from django.shortcuts import get_object_or_404, redirect, render
from .forms import CourseForm, LessonForm
from .models import Courses, Lessons, Questions, TestResults, Tests, UserCourses


def courses_list(request):
  courses = Courses.objects.all().order_by('-create_at')
  return render(
      request, 'learniva_app/courses_list.html', {'courses': courses}
  )

def course_detail(request, course_id):
  course = get_object_or_404(Courses, course_id=course_id)
  lessons = Lessons.objects.filter(courses_course=course).order_by(
      'order_number'
  )
  return render(
      request,
      'learniva_app/course_detail.html',
      {'course': course, 'lessons': lessons},
  )

def test_detail(request, test_id):
  test = get_object_or_404(Tests, pk=test_id)
  # Отримуємо всі питання до цього тесту, сортуючи за порядковим номером
  questions = Questions.objects.filter(tests_test=test).order_by(
      'order_number'
  )

  if request.method == 'POST':
    score = 0
    total_questions = questions.count()
    results_detail = []

    for question in questions:
      # Отримуємо обрану користувачем відповідь з HTML-форми
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


# 6. Видалення курсу
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
      lesson.courses_course = course  # Прив'язуємо урок до конкретного курсу
      lesson.save()
      return redirect('course_detail', course_id=course.course_id)
  else:
    form = LessonForm()

  return render(
      request,
      'learniva_app/add_lesson.html',
      {'form': form, 'course': course},
  )


