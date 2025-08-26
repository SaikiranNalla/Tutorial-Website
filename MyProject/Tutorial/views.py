from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Topic, Subtitle, Concept
# Create your views here.
# To render html pages, to load the database, pass the arguments/data/ to the html page


# def home(request):
#     concepts = Concept.objects.filter(draft=False).order_by('created_at')
#     nav_concepts = concepts
#     return render(request, 'Tutorial/home.html', {
#         "concepts": concepts,
#         "nav_concepts" : nav_concepts,
#         'title': 'Welcome to Tutorial'
#     })

# # To render a Name maybe or a welcome message and button to start
# # def home(request):
# #     return render(request, 'Tutorial/home.html', {
# #         "title": "Welcome to Tutorial"
# #     })

# # To render Contents(title of Topic model/table) of the page
# def index(request, concept_slug):
#     concept = get_object_or_404(Concept, slug=concept_slug, draft=False)
#     topics = Topic.objects.filter(concept=concept, draft=False).order_by('order')

#     concepts = Concept.objects.filter(draft=False).order_by('created_at')
#     nav_concepts = concepts
#     return render(request, 'Tutorial/index.html', {
#         'concept': concept,
#         "topics": topics,
#         "nav_concepts" : nav_concepts,
#     })

# to render specific topic/topic
# it should connect to the index page contents(links)
# those links should dynamically create not hard coded (need to play with GET, POST requests).
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Topic, Subtitle, Concept

def home(request):
    concepts = Concept.objects.filter(draft=False).order_by('created_at')
    nav_concepts = concepts
    return render(request, 'Tutorial/base.html', {
        "concepts": concepts,
        "nav_concepts" : nav_concepts,
        'title': 'Welcome to Tutorial'
    })

def index(request, concept_slug):
    concept = get_object_or_404(Concept, slug=concept_slug, draft=False)
    topics = Topic.objects.filter(concept=concept, draft=False).order_by('order')
    concepts = Concept.objects.filter(draft=False).order_by('created_at')
    nav_concepts = concepts
    return render(request, 'Tutorial/index.html', {
        'concept': concept,
        "topics": topics,
        "nav_concepts" : nav_concepts,
    })

def topic(request, concept_slug, topic_slug):
    current_concept = get_object_or_404(Concept, slug=concept_slug, draft=False)
    topic = get_object_or_404(Topic, slug=topic_slug, concept=current_concept, draft=False)
    topics = Topic.objects.filter(concept=current_concept, draft=False).order_by('order')

    # For sidebar & next/prev
    concept_topics = list(topics)
    previous_topic = None
    next_topic = None

    # For secondary/nav bar concepts
    concepts = Concept.objects.filter(draft=False).order_by('created_at')
    nav_concepts = concepts

    # compute current_topic_index robustly and progress
    current_topic_index = None
    try:
        current_topic_index = concept_topics.index(topic)
        if current_topic_index > 0:
            previous_topic = concept_topics[current_topic_index - 1]
        if current_topic_index < len(concept_topics) - 1:
            next_topic = concept_topics[current_topic_index + 1]
    except ValueError:
        # keep defaults (shouldn't normally happen)
        current_topic_index = 0

    # compute progress percent and textual progress
    total_topics = len(concept_topics) if concept_topics else 0
    if total_topics > 0:
        progress_percent = int(((current_topic_index + 1) / total_topics) * 100)
        current_position = current_topic_index + 1
    else:
        progress_percent = 0
        current_position = 0

    subtitles = topic.subtitles.filter(draft=False).order_by('order')

    context = {
        "nav_concepts": nav_concepts,
        'topics': topics,
        'topic': topic,
        'subtitles': subtitles,
        'concept': current_concept,
        'previous_topic': previous_topic,
        'next_topic': next_topic,
        # NEW: progress + totals for template
        'progress_percent': progress_percent,
        'current_position': current_position,
        'total_topics': total_topics,
    }
    return render(request, 'Tutorial/topic.html', context)
# decorator for verification of admin user
# from django.contrib.admin.views.decorators import staff_member_required
# from .models import Topic
# from .forms import ConceptForm, SubtitleForm
#
# @staff_member_required
# def concept_post(request):
#     if request.method == 'POST':
#         form = ConceptForm(request.POST)
#         if form.is_valid():
#             topic = form.save()
#             return redirect('edit_post', concept_id=topic.id)
#     else:
#         form = ConceptForm()
#     return render(request, 'admin/create_concept.html', {'form':form})
#
#
# @staff_member_required
# def edit_concept(request, concept_id):
#     topic = get_object_or_404(Topic, id=concept_id)
#     if request.method == 'POST':
#         form = ConceptForm(request.POST, instance = topic)
#         if form.is_valid():
#             form.save()
#             return redirect('edit_concept', concept_id=topic.id)
#     else:
#         form = ConceptForm(instance = topic)
#     return render(request, 'admin/edit_concept.html', {"form":form})
#
# @staff_member_required
# def add_subtitle(request, concept_id):
#     topic = get_object_or_404(Topic, id=concept_id)
#     if request.method == 'POST':
#         form = SubtitleForm(request.POST)
#         if form.is_valid():
#             subtitle = form.save(commit=False)
#             subtitle.topic = topic
#             subtitle.save()
#             # If using AJAX, you might return a JSON response here.
#             return redirect('edit_concept', concept_id=topic.id)
#     else:
#         form = SubtitleForm()
#     return render(request, 'admin/add_subtitle.html', {"form":form})