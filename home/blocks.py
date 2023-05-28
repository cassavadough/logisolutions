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
        ('#0b3b5e', 'Royal Blue'),
        ('#ebf1f5', 'Light Blue'),
        ('#f9fafb', 'Gray'),
    ], icon='cup', required=False)
    background_image_width_1920 = ImageChooserBlock(required=False)
    visible = blocks.BooleanBlock(default=True,required=False)

    class Meta:
        abstract = True


class SocialMediaItemBlock(blocks.StructBlock):
    link = blocks.URLBlock()
    social_media = blocks.ChoiceBlock(choices=[
        # ('None', 'None'),
        ('fab fa-facebook-f', 'Facebook'),
        ('fab fa-pinterest-p', 'Twitter'),
        ('fab fa-instagram', 'Instagram'),
        ('fab fa-linkedin', 'LinkedIn'),
    ], icon='cup', required=False)

    class Meta:
        icon = 'user'


class HomeTwoBannerBlockUnit(blocks.StructBlock):
    pre_text = blocks.CharBlock()
    text = blocks.CharBlock(required=False)
    image_619x518 = ImageChooserBlock()
    button_label = blocks.CharBlock(required=False)  # Will determin if Button Shows
    button_page_url = blocks.PageChooserBlock(required=False)


class Image480x700LeftTextRightBlock(BaseBlock):
    image_480x700 = ImageChooserBlock()
    pre_title = blocks.CharBlock()
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    button_label = blocks.CharBlock(required=False)  # Will determin if Button Shows
    button_page_url = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_image_480x700_left_text_right_block.html'
        # max_num = 1


class TwoImages650x682And290x300LeftTextRightBlock(BaseBlock):
    image_650x682 = ImageChooserBlock()
    image_290x300 = ImageChooserBlock()
    pre_title = blocks.CharBlock()
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    button_label = blocks.CharBlock(required=False)  # Will determin if Button Shows
    button_page_url = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_two_images_650x682_290x300_left_text_right_block.html'
        # max_num = 1


class BlurbUnitBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.CharBlock()
    icon_120x120 = blocks.CharBlock()
    image_120x120 = ImageChooserBlock(required=False)
    link_url = blocks.PageChooserBlock(required=False)


    class Meta:
        icon = 'user'
        # template = 'home/blocks/logis_section_blurb_block.html'


class BlurbsBlock(BaseBlock):
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    blurbs = blocks.ListBlock(BlurbUnitBlock())
    # is_list = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_blurbs_block.html'


class CallToActionBlock(BaseBlock):
    text = blocks.CharBlock()
    button_url = blocks.PageChooserBlock(required=False)
    button_label = blocks.CharBlock(required=False)

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
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    people = blocks.ListBlock(
        PersonBlock(),
    )
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_people_block.html'

#
# class PeopleBlock(BaseBlock):
#     title = blocks.CharBlock(required=False)
#     text = blocks.CharBlock(required=False)
#     # people = blocks.ListBlock(
#     #     PersonBlock(),
#     # )
#     button_url = blocks.URLBlock(required=False)
#     button_Label = blocks.CharBlock(required=False)
#
#     class Meta:
#         icon = 'user'
#         template = 'home/blocks/logis_people_block.html'


class TestimonialUnitBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    role = blocks.CharBlock()
    rating = blocks.IntegerBlock()
    message = blocks.CharBlock()
    photo_130x130 = ImageChooserBlock()

    class Meta:
        icon = 'user'
        # template = 'home/blocks/logis_testimonial_unit_block.html'


class TestimonialsBlock(BaseBlock):
    pre_title = blocks.CharBlock()
    title = blocks.CharBlock()
    text = blocks.CharBlock(required=False)
    testimonials = blocks.ListBlock(TestimonialUnitBlock())

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_testimonials_block.html'


class BlogUnitBlock(blocks.StructBlock):
    # title = blocks.CharBlock()
    blog = blocks.ListBlock(blocks.PageChooserBlock(page_type='blog.BlogPage'))
    # ?button_url = blocks.URLBlock(required=False)
    # button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_blog_unit_block.html'


class BlogsBlock(BaseBlock):
    title = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=False)
    blogs = blocks.ListBlock(blocks.PageChooserBlock(page_type='blog.BlogPage'))
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_blogs_block.html'
        # max_num = 1


class NewsUnitBlock(blocks.StructBlock):
    # title = blocks.CharBlock()
    news_item = blocks.PageChooserBlock(page_type='news.NewsPage')
    # ?button_url = blocks.URLBlock(required=False)
    # button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_news_unit_block.html'


class NewsBlock(BaseBlock):
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    # news = blocks.ListBlock(blocks.PageChooserBlock(page_type='news.NewsPage'))
    news = blocks.ListBlock(NewsUnitBlock())
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_news_block.html'
        # max_num = 1


class RichTextBlock(BaseBlock): #Product Description section
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    button_label = blocks.CharBlock(required=False)
    page_url = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_rich_text_block.html'


class ContactUnitAddressBlock(blocks.StructBlock):
    location = blocks.CharBlock()
    phone = blocks.CharBlock()
    text = blocks.CharBlock()


class ContactSectionBlock(blocks.StructBlock):
    addresses = blocks.ListBlock(ContactUnitAddressBlock)

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


class ServiceUnitBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.CharBlock()
    icon = blocks.CharBlock(required=False)
    image_340x230 = ImageChooserBlock()
    # service = blocks.PageChooserBlock(page_type='services.ServicePage')
    # button_url = blocks.URLBlock(required=False)
    # button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_service_unit_block.html'


class ServiceBlock(BaseBlock):
    title = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)

    # # news = blocks.ListBlock(blocks.PageChooserBlock(page_type='news.NewsPage'))
    services = blocks.ListBlock(ServiceUnitBlock())
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_service_block.html'
        # max_num = 1


class ServiceType1Block(BaseBlock):
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    # # news = blocks.ListBlock(blocks.PageChooserBlock(page_type='news.NewsPage'))
    # services = blocks.ListBlock(ServiceUnitBlock())
    # button_url = blocks.URLBlock(required=False)
    # button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_service_type_1_block.html'
        # max_num = 1


class ServiceType2Block(BaseBlock):
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    # # news = blocks.ListBlock(blocks.PageChooserBlock(page_type='news.NewsPage'))
    # services = blocks.ListBlock(ServiceUnitBlock())
    # button_url = blocks.URLBlock(required=False)
    # button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_service_type_2_block.html'
        # max_num = 1


class CheckedListBlock(BaseBlock):
    title = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    list_items = blocks.ListBlock(blocks.CharBlock())

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_checked_list_block.html'
        # max_num = 1


class FAQUnitBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.CharBlock()

    class Meta:
        icon = 'user'
        # template = 'home/blocks/logis_checked_list_block.html'
        # max_num = 1


class FAQBlock(BaseBlock):
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    faq_items = blocks.ListBlock(FAQUnitBlock())

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_faq_block.html'
        # max_num =


class TestimonialFAQComboBlock(BaseBlock):
    title = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    # faq_items = blocks.ListBlock(FAQUnitBlock())

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_faq_block.html'
        # max_num =


class ProductUnitBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    code = blocks.CharBlock()
    image_370x670 = ImageChooserBlock()
    # service = blocks.PageChooserBlock(page_type='services.ServicePage')
    # button_url = blocks.URLBlock(required=False)
    # button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        # template = 'home/blocks/logis_project_unit_block.html'


class ProjectBlock(BaseBlock):
    pre_title = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)

    # # news = blocks.ListBlock(blocks.PageChooserBlock(page_type='news.NewsPage'))
    projects = blocks.ListBlock(ProductUnitBlock())
    button_url = blocks.URLBlock(required=False)
    button_Label = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'home/blocks/logis_project_block.html'
        # max_num = 1