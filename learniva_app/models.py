from django.db import models
import re
from django.conf import settings

class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'courses'
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title


class Lessons(models.Model):
    lessons_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    order_number = models.IntegerField()
    courses_course = models.ForeignKey(Courses, on_delete=models.CASCADE, db_column='courses_course_id')

    class Meta:
        managed = True
        db_table = 'lessons'
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f"{self.courses_course.title} — {self.title}"

    @property
    def embed_url(self):
        if not self.video_url:
            return None
        match = re.search(r'(?:youtu\.be/|v=|embed/)([\w-]{11})', self.video_url)
        return f'https://www.youtube.com/embed/{match.group(1)}' if match else None







class Tests(models.Model):
    test_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    questions_count = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    lessons_lessons = models.ForeignKey(Lessons, on_delete=models.CASCADE, db_column='lessons_lessons_id')

    class Meta:
        managed = True
        db_table = 'tests'
        verbose_name_plural = "Tests"
        

    def __str__(self):
        return self.title


class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=255)
    answers = models.JSONField(blank=True, null=True)
    correct_answer = models.CharField(max_length=100)
    order_number = models.IntegerField()
    tests_test = models.ForeignKey(Tests, on_delete=models.CASCADE, db_column='tests_test_id')

    class Meta:
        managed = True
        db_table = 'questions'
        verbose_name_plural = "questions"

    def __str__(self):
        return self.question_text

class TestResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    score = models.IntegerField()
    complete_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)

    class Meta:
        db_table = 'test_results'
        verbose_name_plural = "Test_results"


class UserCourses(models.Model):
    user_courses_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_courses'
        verbose_name_plural = "User_courses"