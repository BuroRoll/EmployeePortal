# Generated by Django 3.1.7 on 2021-04-05 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_conversation_is_hr_conversation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversation',
            old_name='is_hr_conversation',
            new_name='hr_conversation',
        ),
    ]