from django.db import models
# from django.db.models.fields import CharField


class Books(models.Model):
    testament = models.CharField(max_length=2)
    book = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=10)
    group = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    chapters = models.IntegerField()
    
    def __str__(self):
        return self.book

class Bible(models.Model):
    book_id = models.ForeignKey(Books, on_delete=models.DO_NOTHING)
    chapter = models.IntegerField()
    verse = models.CharField(max_length=5)
    title = models.TextField(null=True)
    text = models.TextField()

    def __str__(self):
        return self.text