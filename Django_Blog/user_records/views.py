from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    return render(request, 'user_records/index.html')


def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics' : topics}
    return render(request, 'user_records/topics.html', context)


def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'user_records/topic.html', context)


def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # Жодних даних не відправлено; створити порожню форму
        form = TopicForm()
    else:
        # відправляємо POST; обробити дані.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_records:topics')

    # Показати порожню або не дійсну форму
    context = {'form' : form}
    return render(request, 'user_records/new_topic.html', context)


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('user_records:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'user_records/new_entry.html', context)


def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)

    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_records:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'user_records/edit_entry.html', context)