# Generated by Django 4.0.3 on 2022-03-17 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testament', models.CharField(max_length=20)),
                ('book', models.CharField(max_length=20)),
                ('abbreviation', models.CharField(max_length=10)),
                ('group', models.CharField(max_length=20)),
                ('chapters', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Bible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verse', models.CharField(max_length=5)),
                ('chapter', models.IntegerField()),
                ('title', models.TextField()),
                ('text', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bible.books')),
            ],
        ),
    ]
