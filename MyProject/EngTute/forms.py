from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Concept, Topic, Subtitle


# Tried to make a html form form to add content in the site but admin page is simple for now
# class ConceptForm(forms.Form):
#     class Meta:
#         model = Topic
#         fields = ['order', 'title', 'slug', 'content', 'has_subtitles']
#
# class SubtitleForm(forms.Form):
#     class Meta:
#         model = Subtitle
#         fields = ['order', 'title', 'slug', 'content']

class ConceptAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    class Meta:
        model = Concept
        fields = '__all__'

class TopicAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    class Meta:
        model = Topic
        fields = '__all__'
        # Automatically adds the slug while entering the title
        prepopulated_fields = {"slug": ("title",)}

class SubtitleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    class Meta:
        model = Subtitle
        fields = '__all__'
        # Getting an error while adding the multiple subtitles because of form validations
        # because slug will generate the unique url/slug while saving and form validation,
        # are before saving method
        # exclude = ('slug',)  # Remove slug from the form so it isn't validated
        # may be later i need to add auto-populate the slug field in the form itself would
        # work for this!
        # prepopulated_fields = {"slug": ("title",)}