from django.urls import path
from . import views

# Define a list fo url Patterns

urlpatterns = [
    # To render Welcome msg
    path('', views.home, name = 'home'),

    # To render all the contents in a Concept model/table
    path('concepts/', views.index, name='index'),

    # to render specific topic
    path('concept/<slug:slug>/', views.topic, name='topic'),
    # TODO: have to create a path for every topic in the database maybe, don't forget o mention the same in MyProject/url.py
]