# Generated by Django 5.0.4 on 2024-05-06 13:53

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caderneta', '0005_mensagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cromo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('posicao', models.CharField(max_length=30)),
                ('imagem', models.CharField(default='/caderneta/Images/Fotos jogadores/default_Player.jpg', max_length=200)),
                ('selecao', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='utilizador',
            name='email',
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='mensagem_texto',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='pub_data',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caderneta.mensagem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caderneta.utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='Pacote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=25)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=5)),
                ('qnt_cromos', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)])),
                ('descricao', models.CharField(max_length=50)),
                ('imagem', models.CharField(default='/caderneta/Images/Pacotes/default_Pacote.jpg', max_length=200)),
                ('cromos', models.ManyToManyField(to='caderneta.cromo')),
            ],
        ),
    ]
