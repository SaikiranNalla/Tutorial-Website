from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Concept, Subtitle
# Create your views here.
# To render html pages, to load the database, pass the arguments/data/ to the html page


# To render a Name maybe or a welcome message and button to start
def home(request):
    return render(request, 'EngTute/home.html', {
        "title": "Welcome to EngTute"
    })

# To render Contents(title of Concept model/table) of the page
def index(request):
    concepts = Concept.objects.all().order_by('order').filter(draft = False)
    return render(request, 'EngTute/index.html', {
        "concepts": concepts
    })

# to render specific topic/concept
# it should connect to the index page contents(links)
# those links should dynamically create not hard coded (need to play with GET, POST requests).
def topic(request, slug):
    # TODO: pass the topic name so that dynamically it shows/loads a page/content for this i used slug, figure out how to use it!
    # form EngTute/urls.py to here, if user type anything in the url bar it will pass it here
    # topic = Concept.
    # return HttpResponse('Welcome to EngTute, Later on we will render a html page using bootstrap')
    concept = get_object_or_404(Concept, slug=slug)
    context = {
        'concept': concept,
        'subtitles': concept.subtitles.all()
    }
    # TODO: Need to change the render page base to specific topic page
    return render(request, 'EngTute/topic.html', context)

# decorator for verification of admin user
# from django.contrib.admin.views.decorators import staff_member_required
# from .models import Concept
# from .forms import ConceptForm, SubtitleForm
#
# @staff_member_required
# def concept_post(request):
#     if request.method == 'POST':
#         form = ConceptForm(request.POST)
#         if form.is_valid():
#             concept = form.save()
#             return redirect('edit_post', concept_id=concept.id)
#     else:
#         form = ConceptForm()
#     return render(request, 'admin/create_concept.html', {'form':form})
#
#
# @staff_member_required
# def edit_concept(request, concept_id):
#     concept = get_object_or_404(Concept, id=concept_id)
#     if request.method == 'POST':
#         form = ConceptForm(request.POST, instance = concept)
#         if form.is_valid():
#             form.save()
#             return redirect('edit_concept', concept_id=concept.id)
#     else:
#         form = ConceptForm(instance = concept)
#     return render(request, 'admin/edit_concept.html', {"form":form})
#
# @staff_member_required
# def add_subtitle(request, concept_id):
#     concept = get_object_or_404(Concept, id=concept_id)
#     if request.method == 'POST':
#         form = SubtitleForm(request.POST)
#         if form.is_valid():
#             subtitle = form.save(commit=False)
#             subtitle.concept = concept
#             subtitle.save()
#             # If using AJAX, you might return a JSON response here.
#             return redirect('edit_concept', concept_id=concept.id)
#     else:
#         form = SubtitleForm()
#     return render(request, 'admin/add_subtitle.html', {"form":form})