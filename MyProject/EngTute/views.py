from django.shortcuts import render, get_object_or_404
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
    concepts = Concept.objects.all().order_by('order')
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
    content = get_object_or_404(Concept, slug=slug)
    # TODO: Need to change the render page base to specific topic page
    return render(request, 'EngTute/base.html', {
        "slug":content.slug,
        "title":content.title
    })