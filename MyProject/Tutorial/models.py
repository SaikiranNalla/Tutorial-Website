from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Concept(models.Model):
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True,
                            help_text="URL-friendly identifier; auto-generated")
    draft = models.BooleanField(default=False,
                                help_text="Tick if this topic should remain in draft not show up in live site)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if blank
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Topic(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='topics')
    order       = models.PositiveIntegerField(help_text="Controls display order")
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True, blank=True,
                                   help_text="URL-friendly identifier; auto-generated")
    # content = CKEditor5Field()
    content = CKEditor5Field(config_name='default', default='')
    # You can edit the ckeditor text field, dig around
    # The optional config_name parameter should match the key in your CKEDITOR_5_CONFIGS settings.
    # Do the same for the Subtitle model or any other place where you previously used the old CKEditor field. '''
    # has_subtitles = models.BooleanField(default=False)
    draft = models.BooleanField(default=False,
                                help_text="Tick if this topic should remain in draft not show up in live site)")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if blank
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}. {self.title}"

class Subtitle(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtitles')
    order       = models.PositiveIntegerField(help_text="Controls display order")
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True, blank=True,
                                   help_text="URL-friendly identifier; auto-generated")
    content = CKEditor5Field(config_name='default', default='')
    draft = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ['topic', 'slug']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if blank
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.topic.title} - {self.order}. {self.title}"