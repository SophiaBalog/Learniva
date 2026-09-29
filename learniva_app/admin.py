from django.contrib import admin
from .models import Courses,UserCourses,Users,TestResults,Tests,Questions,Lessons

# Register your models here.


admin.site.register(Courses)
admin.site.register(Users)
admin.site.register(Lessons)
admin.site.register(UserCourses)
admin.site.register(Tests)
admin.site.register(Questions)
admin.site.register(TestResults)