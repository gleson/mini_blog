# Generated by Django 4.1 on 2023-08-28 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Books",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("testament", models.CharField(max_length=2)),
                ("book", models.CharField(max_length=20)),
                ("abbreviation", models.CharField(max_length=10)),
                ("group", models.CharField(max_length=20)),
                ("slug", models.SlugField(unique=True)),
                ("chapters", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Bible",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("chapter", models.IntegerField()),
                ("verse", models.CharField(max_length=5)),
                ("title", models.TextField(null=True)),
                ("text", models.TextField()),
                (
                    "book_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="bible.books"
                    ),
                ),
            ],
        ),
    ]
