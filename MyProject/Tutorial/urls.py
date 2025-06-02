from django.urls import path
from . import views

# Define a list fo url Patterns

urlpatterns = [
    # To render Welcome msg
    path('', views.home, name = 'home'),

    # To render all the contents in a Topic model/table
    path('<slug:concept_slug>/', views.index, name='index'),

    # to render specific topic
    path('<slug:concept_slug>/<slug:topic_slug>/', views.topic, name='topic'),
    # TODO: have to create a path for every topic in the database maybe, don't forget o mention the same in MyProject/url.py
    # path('post/', views.post, name="post")
    # path('ckeditr')
]