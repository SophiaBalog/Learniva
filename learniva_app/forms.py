from django import forms
from .models import Courses, Lessons


class CourseForm(forms.ModelForm):

  class Meta:
    model = Courses
    fields = ['title', 'description', 'category', 'image']
    widgets = {
        'title': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Назва курсу'}
        ),
        'description': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опис курсу',
            }
        ),
        'category': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Категорія'}
        ),
        'image': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'URL або шлях до зображення',
            }
        ),
    }


class LessonForm(forms.ModelForm):

  class Meta:
    model = Lessons
    # Приховуємо поле courses_course, бо курс буде підставлятися автоматично у view
    fields = ['title', 'content', 'video_url', 'order_number']
    widgets = {
        'title': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Назва уроку'}
        ),
        'content': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Текст уроку',
            }
        ),
        'video_url': forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/...',
            }
        ),
        'order_number': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Порядковий номер (1, 2, 3...)',
            }
        ),
    }