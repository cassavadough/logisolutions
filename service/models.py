from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from home import blocks
from home.models import MONTH_CHOICES, DAY_CHOICES
import datetime
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from home import blocks

@register_snippet
class ServiceCategory(models.Model):
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
        verbose_name_plural = 'blog categories'


class ServiceIndexPage(Page):
    subpage_types = ['service.ServicePage', ]
    max_count = 1
    # intro = RichTextField(blank=True)
    intro = models.CharField(max_length=120, null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner_image'),
    ]

    template = 'shared_templates/index_page_template.html'

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = ServicePage.objects.live().public().order_by('-first_published_at')
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

        context['item_type'] = 'service'

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["items"] = posts
        # context["items"] = all_posts
        return context
    #
    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #
    #     # Add extra variables and return the updated context
    #     context['item_type'] = 'service'
    #     context['items'] = ServicePage.objects.child_of(self).live()
    #     return context
        

class ServicePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ServicePage', related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ServicePage(Page):
    page_description = "Use this page for all Service related pages"
    parent_page_types = ['service.ServiceIndexPage']
    # author = models.CharField(max_length=50, null=True, blank=True)
    # date = models.DateField("End date")
    # month_published = models.CharField(max_length=4, choices=MONTH_CHOICES, default='JAN', null=True, blank=True)
    # day_published = models.CharField(max_length=5, choices = DAY_CHOICES, default='01', null=True, blank=True)
    # service_date = models.DateField("Service date", default=datetime.datetime.now)
    # start_date_time = models.DateTimeField(verbose_name='Start Date & Time',default=datetime.datetime.now)
    # end_date_time = models.DateTimeField(verbose_name="End Date & Time",default=datetime.datetime.now)
    intro = models.CharField(max_length=250, blank=True, null=True,)
    # info = RichTextField()
    # on_front_page = models.BooleanField(default=False, null=True, blank=True)
    feature_image_340x230 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        null = True, blank = True
    )
    body = StreamField([
        ('richtext_block', blocks.RichTextBlock(required=False)),

    ], use_json_field=True, collapsed=True, blank=True, null=True)
    tags = ClusterTaggableManager(through=ServicePageTag, blank=True)
    categories = ParentalManyToManyField('service.ServiceCategory', blank=True)
    item_type = models.CharField(max_length=10, default='Service', null=True, blank=True)

    content_panels = Page.content_panels + [
        # FieldPanel('author'),
        FieldPanel('intro'),
        FieldPanel('body'),
        # FieldPanel('on_front_page'),
        FieldPanel('feature_image_340x230'),
    ]

    template = 'shared_templates/page_template.html'


class ServicePageGalleryImage(Orderable):
    page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name='gallery_images')

    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.PROTECT, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]