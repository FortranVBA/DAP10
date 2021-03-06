# Generated by Django 3.2.4 on 2021-06-19 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, max_length=2048)),
                ('type', models.CharField(max_length=128)),
                ('author_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.person')),
            ],
        ),
    ]
