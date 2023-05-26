from wagtail import blocks, embeds
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

# class BaseBlock(blocks.StructBlock):
#     name = blocks.CharBlock()
#     default_background = blocks.ChoiceBlock(choices=[
#         # ('None', 'None'),
#         ('my_facility_bg', 'Blue'),
#         ('my_testimonial_bg', 'Pink'),
#         ('my_counter_bg', 'Orange'),
#     ], icon='cup', required=False)
#     background_image_1920x622 = ImageChooserBlock(required=False)
#     visible = blocks.BooleanBlock(required=False)

#     class Meta:
#         abstract = True


class BaseBlock(blocks.StructBlock):
    admin_label = blocks.CharBlock()
    is_background_color = blocks.BooleanBlock(required=False)
    #f9fafb;
    default_background = blocks.ChoiceBlock(choices=[
        ('#ffffff', 'White'),
        ('#0b3b5e', 'Blue'),
        ('#f9fafb', 'Gray'),
    ], icon='cup', required=False)
    background_image_width_1920 = ImageChooserBlock(required=False)
    visible = blocks.BooleanBlock(required=False)

    class Meta:
        abstract = True


class SocialMediaItemBlock(blocks.StructBlock):
    link = blocks.URLBlock()
    social_media = blocks.ChoiceBlock(choices=[
        # ('None', 'None'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
    ], icon='cup', required=False)

    class Meta:
        icon = 'user'


class HomeTwoBannerBlockUnit(blocks.StructBlock):
    pre_text = blocks.CharBlock()
    text = blocks.CharBlock(required=False)
    image_619x518 = ImageChooserBlock()
    button_label = blocks.CharBlock()  # Will determin if Button Shows
    button_page_url = blocks.PageChooserBlock(required=False)


class Image480x700LeftTextRightBlock(BaseBlock):
    image_480x700 = ImageChooserBlock()
    pre_title = blocks.CharBlock()
    title = blocks.CharBlock()
    text = blocks.CharBlock()
    utton_label = blocks.CharBlock()  # Will determin if Button Shows
    button_page_url = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_image_480x700_left_text_right_block.html'
        max_num = 1


class BlurbBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.CharBlock()
    icon_100x100 = ImageChooserBlock(required=False)
    image_340x230 = ImageChooserBlock()
    read_more = blocks.PageChooserBlock()

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_section_blurb_block.html'


class BlurbsBlock(BaseBlock):
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    blurbs = blocks.ListBlock(BlurbBlock())

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_blurbs_block.html'


class CallToActionBlock(BaseBlock):
    text = blocks.CharBlock()
    button_url = blocks.PageChooserBlock()
    button_Label = blocks.CharBlock()

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_call_to_action_block.html'


class PersonBlock(blocks.StructBlock):
    full_name = blocks.CharBlock()
    role = blocks.CharBlock()
    photo_270x420 = ImageChooserBlock()
    page_url = blocks.PageChooserBlock(required=False)
    social_media_links = blocks.ListBlock(SocialMediaItemBlock(), required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_person_block.html'


class PeopleBlock(BaseBlock):
    title = blocks.CharBlock(required=False)
    intro_text = blocks.CharBlock(required=False)
    people = blocks.ListBlock(
        PersonBlock(),
    )
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_people_block.html'


class TestimonialBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    role = blocks.CharBlock()
    rating = blocks.IntegerBlock()
    message = blocks.CharBlock()
    photo_130x130 = ImageChooserBlock()

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_testimonial_block.html'


class TestimonialsBlock(BaseBlock):
    pre_title = blocks.CharBlock()
    title = blocks.CharBlock()
    text = blocks.CharBlock()
    testimonials = blocks.ListBlock(TestimonialBlock())

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_testimonials_block.html'


class BlogsBlock(BaseBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    blogs = blocks.ListBlock(blocks.PageChooserBlock(page_type='blog.BlogPage'))
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_blogs_block.html'
        # max_num = 1


class NewsBlock(BaseBlock):
    pre_title = blocks.CharBlock()
    title = blocks.CharBlock()
    news = blocks.ListBlock(blocks.PageChooserBlock(page_type='news.NewsPage'))
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_news_block.html'
        # max_num = 1


class RichTextBlock(BaseBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    button_label = blocks.CharBlock(required=False)
    page_url = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/leud_rich_text_block.html'


class ContactSectionAddressBlockUnit(blocks.StructBlock):
    location = blocks.CharBlock()
    text = blocks.RichTextBlock(required=False)


class ContactSectionBlock(blocks.StructBlock):
    addresses = blocks.ListBlock(ContactSectionAddressBlockUnit)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_contact_section_block.html'


class SponsorsSliderBlock(BaseBlock):
    title = blocks.CharBlock(required=False)
    sponsors = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_sponsors_slider_block.html'
        max_num = 1


