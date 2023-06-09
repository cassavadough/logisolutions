from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks as wagtail_blocks
# from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from home import blocks
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail import blocks as wagtail_blocks
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.forms import FormBuilder
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
# from wagtail.contrib.settings.models import (
#     BaseGenericSetting,
#     BaseSiteSetting,
#     register_setting,
# )

MONTH_CHOICES = (
    ('JAN','January'),
    ('FEB','February'),
    ('MAR','March'),
    ('APR','April'),
    ('MAY','May'),
    ('JUN','June'),
    ('JUL','July'),
    ('AUG','August'),
    ('SEP','September'),
    ('OCT','October'),
    ('NOV','November'),
    ('DEC','December'),
)

DAY_CHOICES = (
    ('01','1st'), ('02','2nd'), ('03','3rd'), ('04','4th'), ('06','6th'),
    ('07','07th'), ('08','8th'), ('09','9th'), ('10','10th'),  ('11','11th'),
    ('12','12th'), ('13','13th'), ('14','14th'), ('15','15th'),
    ('16','16th'), ('17','17th'), ('18','18th'), ('19','19th'), ('20','20th'),
    ('21','21st'), ('22','22nd'), ('23','23rd'), ('24','24th'), ('25','25th'),
    ('26','26th'), ('27','27th'),   ('28','28th'), ('29','29th'), ('30','30th'), ('31','31st'),

)

PAGE_TEMPLATE = (
    ('general','General'),
    ('service','Service'),
    ('product','Product'),
    ('team','Team'),

)

from wagtailcaptcha.models import WagtailCaptchaEmailForm

# @register_setting
# class BackgroundColorGraySettings(BaseGenericSetting):
#     color = models.CharField()
#
#
# @register_setting
# class BackgroundColorGoldSettings(BaseGenericSetting):
#     color = models.CharField()
#
#
# @register_setting
# class BackgroundColorGreenSettings(BaseGenericSetting):
#     color = models.CharField()


# class HomePage(Page):
#     pass

class HomePage(Page):
    # max_count = 1
    # title = models.CharField(max_length=200)

    body = StreamField([
        ('richtext_block', blocks.RichTextBlock(required=False)),
        ('Services_block', blocks.ServiceBlock(required=False)),
        ('left_image_and_text_block', blocks.Image480x700LeftTextRightBlock(required=False)),
        ('two_images_left_and_text_right_block', blocks.TwoImages650x682And290x300LeftTextRightBlock(required=False)),
        ('call_to_action_block', blocks.CallToActionBlock(required=False)),
        ('people_block', blocks.PeopleBlock(required=False)),
        ('sponsors_slider_block', blocks.SponsorsSliderBlock(required=False)),
        ('news_block', blocks.NewsBlock(required=False)),
        ('testimonial_block', blocks.TestimonialsBlock(required=False)),
        ('blurb_block', blocks.BlurbsBlock(required=False)),
        ('frequestly_asked_questions_block', blocks.FAQBlock(required=False)),
        ('project_block', blocks.ProjectBlock(required=False)),

    ], use_json_field=True, collapsed=True,  blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Add extra variables and return the updated context
        context['is_home'] = True
        return context

    class Meta:
        verbose_name = "Home Page"


class FlexPage(Page):
    template = 'flex_page/flex_page.html'
    logis_page_template = models.CharField(max_length=30, choices=PAGE_TEMPLATE, blank=True, null=True, default='general')
    intro = models.CharField(max_length=250)
    feature_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True
    )
    banner_background_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True
    )

    body = StreamField([
        ('richtext_block', blocks.RichTextBlock(required=False)),
        ('Services_block', blocks.ServiceBlock(required=False)),
        ('left_image_and_text_block', blocks.Image480x700LeftTextRightBlock(required=False)),
        ('two_images_left_and_text_right_block', blocks.TwoImages650x682And290x300LeftTextRightBlock(required=False)),
        ('call_to_action_block', blocks.CallToActionBlock(required=False)),
        ('people_block', blocks.PeopleBlock(required=False)),
        ('sponsors_slider_block', blocks.SponsorsSliderBlock(required=False)),
        ('news_block', blocks.NewsBlock(required=False)),
        ('testimonial_block', blocks.TestimonialsBlock(required=False)),
        ('blurb_block', blocks.BlurbsBlock(required=False)),
        ('frequestly_asked_questions_block', blocks.FAQBlock(required=False)),
        ('project_block', blocks.ProjectBlock(required=False)),

    ], use_json_field=True, collapsed=True, blank=True, null=True)

    def get_context(self, request, *args, **kwargs):
        # this_page_type=None

        context = super().get_context(request, *args, **kwargs)

        # Add extra variables and return the updated context
        return context

    content_panels = Page.content_panels + [
        FieldPanel('banner_background_image'),
        FieldPanel('intro'),
        FieldPanel('logis_page_template'),
        FieldPanel('feature_image'),
        FieldPanel('body'),
    ]


class CustomFormBuilder(FormBuilder):

    def get_create_field_function(self, type):
        """
        Override the method to prepare a wrapped function that will call the original
        function (which returns a field) and update the widget's attrs with a custom
        value that can be used within the template when rendering each field.
        """

        create_field_function = super().get_create_field_function(type)

        def wrapped_create_field_function(field, options):
            created_field = create_field_function(field, options)
            created_field.widget.attrs.update(
                    # {"class": field.field_classname} # Important: using the class may be sufficient, depending on how your form is being rendered, try this first.
                    {"class": 'form-control'}, # this is a non-standard attribute and will require custom template rendering of your form to work
                    # {"placeholder": field.placeholder},
                )

            return created_field

        return wrapped_create_field_function


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['position'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['job_description'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['gender'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['job_location_primary_region'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['country'].widget.attrs.update({'class': 'form-control'})


class FormPage(WagtailCaptchaEmailForm):
# class FormPage(AbstractEmailForm):
    form_builder = CustomFormBuilder
    # template = "contact_form_page"

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]



