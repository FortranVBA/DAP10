# Generated by Django 3.2.4 on 2021-06-19 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('desc', models.TextField(blank=True, max_length=2048)),
                ('tag', models.CharField(max_length=128)),
                ('priority', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=128)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assigned_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to='account.person')),
                ('author_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='account.person')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
