# Generated by Django 4.2.1 on 2023-05-27 10:00

import datetime
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcore', '0083_workflowcontenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name_plural': 'blog categories',
            },
        ),
        migrations.CreateModel(
            name='NewsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('author', models.CharField(blank=True, max_length=50, null=True)),
                ('month_published', models.CharField(blank=True, choices=[('JAN', 'January'), ('FEB', 'February'), ('MAR', 'March'), ('APR', 'April'), ('MAY', 'May'), ('JUN', 'June'), ('JUL', 'July'), ('AUG', 'August'), ('SEP', 'September'), ('OCT', 'October'), ('NOV', 'November'), ('DEC', 'December')], default='JAN', max_length=4, null=True)),
                ('day_published', models.CharField(blank=True, choices=[('01', '1st'), ('02', '2nd'), ('03', '3rd'), ('04', '4th'), ('06', '6th'), ('07', '07th'), ('08', '8th'), ('09', '9th'), ('10', '10th'), ('11', '11th'), ('12', '12th'), ('13', '13th'), ('14', '14th'), ('15', '15th'), ('16', '16th'), ('17', '17th'), ('18', '18th'), ('19', '19th'), ('20', '20th'), ('21', '21st'), ('22', '22nd'), ('23', '23rd'), ('24', '24th'), ('25', '25th'), ('26', '26th'), ('27', '27th'), ('28', '28th'), ('29', '29th'), ('30', '30th'), ('31', '31st')], default='01', max_length=5, null=True)),
                ('news_date', models.DateField(default=datetime.datetime.now, verbose_name='News date')),
                ('body', wagtail.fields.StreamField([('richtext_block', wagtail.blocks.StructBlock([('admin_label', wagtail.blocks.CharBlock()), ('is_background_color', wagtail.blocks.BooleanBlock(required=False)), ('default_background', wagtail.blocks.ChoiceBlock(choices=[('#ffffff', 'White'), ('#0b3b5e', 'Royal Blue'), ('#0b3b5e', 'Light Blue'), ('#f9fafb', 'Gray')], icon='cup', required=False)), ('background_image_width_1920', wagtail.images.blocks.ImageChooserBlock(required=False)), ('visible', wagtail.blocks.BooleanBlock(required=False)), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('button_label', wagtail.blocks.CharBlock(required=False)), ('page_url', wagtail.blocks.PageChooserBlock(required=False))], required=False))], blank=True, null=True, use_json_field=True)),
                ('item_type', models.CharField(blank=True, default='News', max_length=10, null=True)),
                ('categories', modelcluster.fields.ParentalManyToManyField(blank=True, to='news.newscategory')),
                ('feature_image_330x330', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('main_image_1024x683', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsPageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='news.newspage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsPageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='news.newspage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newspage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='news.NewsPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='NewsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.CharField(blank=True, max_length=120, null=True)),
                ('banner_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
