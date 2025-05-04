from django.contrib import admin

from .models import Concept, Subtitle
from .forms import ConceptAdminForm, SubtitleAdminForm

# Register your models here.
# admin.site.register(Concept)
# admin.site.register(Subtitle)

# In-line subtitle which is used to maintain subtitle in the Concepts model itself
# and we mentioned as a inline for this model we no need to register seperately
class SubtitleInline(admin.StackedInline):
    model = Subtitle
    form = SubtitleAdminForm
    # Automatically adds the slug while entering the title
    # TODO: same functionality for ConceptAdminForm! (Automatic slug display)
    prepopulated_fields = {"slug": ("title",)}
    extra = 0 # If you need default subtitle field value should be '1'

# Custom admin class to register the model
@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    form = ConceptAdminForm
    # Automatically adds the slug while entering the title
    # prepopulated_fields = {"slug": ("title",)}
    inlines = [SubtitleInline]
    list_display = ('order', 'title', 'draft')
    list_display_links = ('title',) # The 'title' column becomes a link for edit option