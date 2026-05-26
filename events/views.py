from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
import json

from .models import Event, Registration, Comment, Category
from .forms import EventForm, CommentForm


def index(request):
    upcoming = Event.objects.filter(date__gte=timezone.now(), is_active=True).order_by('date')[:6]
    past = Event.objects.filter(date__lt=timezone.now(), is_active=True).order_by('-date')[:3]
    categories = Category.objects.all()
    return render(request, 'events/index.html', {
        'upcoming': upcoming,
        'past': past,
        'categories': categories,
    })


def event_list(request):
    events = Event.objects.filter(is_active=True)
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    time_filter = request.GET.get('time', 'upcoming')

    if q:
        events = events.filter(
            Q(title__icontains=q) | Q(book_title__icontains=q) | Q(book_author__icontains=q)
        )
    if category_id:
        events = events.filter(category_id=category_id)
    if time_filter == 'past':
        events = events.filter(date__lt=timezone.now()).order_by('-date')
    else:
        events = events.filter(date__gte=timezone.now()).order_by('date')

    categories = Category.objects.all()
    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'q': q,
        'selected_category': category_id,
        'time_filter': time_filter,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(event=event, user=request.user).exists()
    comments = event.comments.filter(parent=None).prefetch_related('replies__user')
    comment_form = CommentForm()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    if request.method == 'POST':
        if event.is_full:
            return JsonResponse({'status': 'error', 'message': 'Мероприятие заполнено'})
        reg, created = Registration.objects.get_or_create(event=event, user=request.user)
        if created:
            return JsonResponse({'status': 'ok', 'message': 'Вы успешно зарегистрированы!',
                                  'count': event.participants_count})
        else:
            return JsonResponse({'status': 'info', 'message': 'Вы уже зарегистрированы'})
    return redirect('event_detail', pk=pk)


@login_required
def event_unregister(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        Registration.objects.filter(event=event, user=request.user).delete()
        return JsonResponse({'status': 'ok', 'message': 'Регистрация отменена',
                              'count': event.participants_count})
    return redirect('event_detail', pk=pk)


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            messages.success(request, 'Мероприятие успешно создано!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Создать мероприятие'})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, author=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Мероприятие обновлено!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Редактировать'})


@login_required
def add_comment(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        parent_id = data.get('parent_id')
        if not text:
            return JsonResponse({'status': 'error', 'message': 'Пустой комментарий'})
        comment = Comment.objects.create(
            event=event, user=request.user, text=text,
            parent_id=parent_id if parent_id else None
        )
        return JsonResponse({
            'status': 'ok',
            'id': comment.id,
            'text': comment.text,
            'user': comment.user.get_full_name() or comment.user.username,
            'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
            'parent_id': parent_id,
        })
    return JsonResponse({'status': 'error'}, status=400)


def search_api(request):
    q = request.GET.get('q', '')
    if len(q) < 2:
        return JsonResponse({'results': []})
    events = Event.objects.filter(
        Q(title__icontains=q) | Q(book_title__icontains=q),
        is_active=True, date__gte=timezone.now()
    )[:5]
    results = [{'id': e.id, 'title': e.title, 'date': e.date.strftime('%d.%m.%Y')} for e in events]
    return JsonResponse({'results': results})


@login_required
def my_events(request):
    organized = Event.objects.filter(author=request.user, is_active=True).order_by('-date')
    registered = Event.objects.filter(
        registrations__user=request.user, is_active=True
    ).order_by('date')
    return render(request, 'events/my_events.html', {
        'organized': organized,
        'registered': registered,
    })
