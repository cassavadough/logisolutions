from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from home.models import MONTH_CHOICES, DAY_CHOICES
import datetime
import home.models
from home import blocks
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


@register_snippet
class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'project categories'


class ProjectIndexPage(Page):
    subpage_types = ['project.ProjectPage', ]
    max_count = 1
    intro = models.CharField(max_length=120, null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner_image'),
    ]
    subpage_types = ['project.ProjectPage']

    template = 'shared_templates/index_page_template.html'

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = ProjectPage.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 6)
        # Try to get the ?page=x value
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        context['item_type'] = 'project'

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["items"] = posts
        # context["items"] = all_posts
        return context


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProjectPage', related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ProjectPage(Page):
    parent_page_types = ['project.ProjectIndexPage']
    page_description = "Use this page for all Project Pages"
    # author = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(verbose_name='Start Date & Time',default=datetime.datetime.now)
    completion_date = models.DateField(verbose_name="End Date & Time",default=datetime.datetime.now)
    intro = models.CharField(max_length=120)
    client = models.CharField(max_length=120)
    website = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    on_front_page = models.BooleanField(default=False, null=True, blank=True)
    feature_image_list_370x570 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        null=True, blank=True
    )
    feature_image_detail_1300x650 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        null=True, blank=True
    )
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)
    categories = ParentalManyToManyField('project.ProjectCategory', blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('start_date'),
        FieldPanel('completion_date'),
        FieldPanel('body'),
        FieldPanel('goal'),
        FieldPanel('achieved'),
        FieldPanel('start_month'),
        FieldPanel('start_day'),
        # FieldPanel('on_front_page'),
        FieldPanel('feature_image_570x400'),
        # FieldPanel('on_front_page'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    parent_page_types = ['project.ProjectIndexPage']

    # class Meta:
    #     verbose_name = "Project Page"
    template = 'shared_templates/page_template.html'

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = ProjectPage.objects.live().public().order_by('-first_published_at')[:5]
        context["items"] = all_posts
        # context["items"] = all_posts
        return context


class ProjectPageGalleryImage(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name='gallery_images')

    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]