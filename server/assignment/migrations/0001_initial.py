# Generated by Django 5.0.3 on 2025-04-15 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=105)),
                ('description', models.TextField()),
                ('from_date', models.DateTimeField(auto_now_add=True)),
                ('submission_date', models.DateTimeField()),
            ],
        ),
    ]
