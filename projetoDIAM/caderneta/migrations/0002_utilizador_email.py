# Generated by Django 5.0.4 on 2024-04-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caderneta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilizador',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
    ]
