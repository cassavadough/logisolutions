# Generated by Django 4.2.1 on 2023-05-28 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_flexpage_page_template_alter_flexpage_body'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flexpage',
            old_name='page_template',
            new_name='logis_page_template',
        ),
    ]
