# Generated by Django 3.2.2 on 2021-05-13 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_course_user_set'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='user_set',
            new_name='user',
        ),
    ]
