from django import forms
from django.core.exceptions import ValidationError
from .models import Courses, Lessons, Tests, Questions




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



class TestForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва тесту'})}


class QuestionForm(forms.ModelForm):
    answers_text = forms.CharField(
        label='Варіанти відповідей',
        help_text='Кожен варіант з нового рядка (мінімум 2)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
    )

    class Meta:
        model = Questions
        fields = ['question_text', 'correct_answer', 'order_number']

    def clean(self):
        cleaned = super().clean()
        answers = [a.strip() for a in cleaned.get('answers_text', '').splitlines() if a.strip()]
        correct = (cleaned.get('correct_answer') or '').strip()

        if len(answers) < 2:
            raise ValidationError('Потрібно щонайменше два варіанти відповіді.')
        if correct not in answers:
            raise ValidationError('Правильна відповідь має збігатися з одним із варіантів.')

        cleaned['answers'] = answers
        cleaned['correct_answer'] = correct
        return cleaned

    def save(self, commit=True):
        question = super().save(commit=False)
        question.answers = self.cleaned_data['answers']
        if commit:
            question.save()
        return question