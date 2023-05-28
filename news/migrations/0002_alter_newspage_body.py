# Generated by Django 4.2.1 on 2023-05-27 14:34

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='body',
            field=wagtail.fields.StreamField([('richtext_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#ebf1f5', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(required=False)), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('button_label', wagtail.blocks.CharBlock(required=False)), ('page_url', wagtail.blocks.PageChooserBlock(required=False))], required=False))], blank=True, null=True, use_json_field=True),
        ),
    ]
