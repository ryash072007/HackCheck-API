# Generated by Django 5.1.7 on 2025-03-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='number',
            field=models.IntegerField(unique=True),
        ),
    ]
