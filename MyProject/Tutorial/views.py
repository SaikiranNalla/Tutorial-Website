from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Topic, Subtitle, Concept
# Create your views here.
# To render html pages, to load the database, pass the arguments/data/ to the html page


def home(request):
    concepts = Concept.objects.filter(draft=False).order_by('created_at')
    nav_concepts = concepts
    return render(request, 'Tutorial/base.html', {
        "concepts": concepts,
        "nav_concepts" : nav_concepts,
        'title': 'Welcome to Tutorial'
    })

# To render a Name maybe or a welcome message and button to start
# def home(request):
#     return render(request, 'Tutorial/home.html', {
#         "title": "Welcome to Tutorial"
#     })

# To render Contents(title of Topic model/table) of the page
def index(request, concept_slug):
    concept = get_object_or_404(Concept, slug=concept_slug, draft=False)
    topics = Topic.objects.filter(concept=concept, draft=False).order_by('order')
    return render(request, 'Tutorial/index.html', {
        'concept': concept,
        "topics": topics
    })

# to render specific topic/topic
# it should connect to the index page contents(links)
# those links should dynamically create not hard coded (need to play with GET, POST requests).
def topic(request, concept_slug, topic_slug):
    # TODO: pass the topic name so that dynamically it shows/loads a page/content for this i used slug, figure out how to use it!
    # form Tutorial/urls.py to here, if user type anything in the url bar it will pass it here
    # topic = Topic.
    # return HttpResponse('Welcome to Tutorial, Later on we will render a html page using bootstrap')
    current_concept = get_object_or_404(Concept, slug=concept_slug, draft = False)
    topic = get_object_or_404(Topic, slug=topic_slug, concept = current_concept, draft= False)
    topics = Topic.objects.filter(concept=current_concept, draft=False).order_by('order')

    # 3. Get ALL Topics for the current concept, ordered (for sidebar AND next/prev buttons)
    # Convert to list for efficient indexing
    concept_topics = list(Topic.objects.filter(concept=current_concept, draft=False).order_by('order'))

    # 4. Find the current topic's position in the ordered list
    previous_topic = None
    next_topic = None

    try:
        current_topic_index = concept_topics.index(topic)

        # Calculate previous topic
        if current_topic_index > 0:
            previous_topic = concept_topics[current_topic_index - 1]

        # Calculate next topic
        if current_topic_index < len(concept_topics) - 1:
            next_topic = concept_topics[current_topic_index + 1]

    except ValueError:
        # This case should ideally not happen if 'topic' was successfully fetched
        # from 'concept_topics' list, but it's good for robustness.
        pass

    subtitles = topic.subtitles.filter(draft=False).order_by('order')
    context = {
        'topics': topics,
        'topic': topic,
        'subtitles': subtitles,
        'concept': current_concept,
        'previous_topic': previous_topic,
        'next_topic': next_topic,
    }
    # TODO: Need to change the render page base to specific topic page
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