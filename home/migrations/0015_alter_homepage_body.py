# Generated by Django 4.2.1 on 2023-05-27 17:34

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('richtext_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#ebf1f5', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(default=True, required=False)), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('button_label', wagtail.blocks.CharBlock(required=False)), ('page_url', wagtail.blocks.PageChooserBlock(required=False))], required=False)), ('Services_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#ebf1f5', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(default=True, required=False)), ('title', wagtail.blocks.CharBlock(required=False)), ('text', wagtail.blocks.CharBlock(required=False)), ('services', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.CharBlock()), ('icon', wagtail.blocks.CharBlock(required=False)), ('image_340x230', wagtail.images.blocks.ImageChooserBlock())]))), ('button_url', wagtail.blocks.URLBlock(required=False)), ('button_Label', wagtail.blocks.CharBlock(required=False))], required=False)), ('left_image_and_text_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#ebf1f5', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(default=True, required=False)), ('image_480x700', wagtail.images.blocks.ImageChooserBlock()), ('pre_title', wagtail.blocks.CharBlock()), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('button_label', wagtail.blocks.CharBlock(required=False)), ('button_page_url', wagtail.blocks.PageChooserBlock(required=False))], required=False)), ('two_images_left_and_text_right_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#ebf1f5', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(default=True, required=False)), ('image_650x682', wagtail.images.blocks.ImageChooserBlock()), ('image_290x300', wagtail.images.blocks.ImageChooserBlock()), ('pre_title', wagtail.blocks.CharBlock()), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('button_label', wagtail.blocks.CharBlock(required=False)), ('button_page_url', wagtail.blocks.PageChooserBlock(required=False))], required=False)), ('call_to_action_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#ebf1f5', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(default=True, required=False)), ('text', wagtail.blocks.CharBlock()), ('button_url', wagtail.blocks.PageChooserBlock(required=False)), ('button_label', wagtail.blocks.CharBlock(required=False))], required=False)), ('people_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#ebf1f5', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(default=True, required=False)), ('pre_title', wagtail.blocks.CharBlock(required=False)), ('title', wagtail.blocks.CharBlock(required=False)), ('people', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('full_name', wagtail.blocks.CharBlock()), ('role', wagtail.blocks.CharBlock()), ('photo_270x420', wagtail.images.blocks.ImageChooserBlock()), ('page_url', wagtail.blocks.PageChooserBlock(required=False)), ('social_media_links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('link', wagtail.blocks.URLBlock()), ('social_media', wagtail.blocks.ChoiceBlock(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('linkedin', 'LinkedIn')], icon='cup', required=False))]), required=False))]))), ('button_url', wagtail.blocks.URLBlock(required=False)), ('button_Label', wagtail.blocks.CharBlock(required=False))], required=False))], blank=True, null=True, use_json_field=True),
        ),
    ]
