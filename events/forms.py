from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'book_title', 'book_author',
                  'cover_image', 'date', 'duration_minutes', 'format',
                  'stream_link', 'max_participants']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название мероприятия'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'book_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название книги'}),
            'book_author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Автор книги'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'format': forms.Select(attrs={'class': 'form-control'}),
            'stream_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш комментарий...'
    }))
