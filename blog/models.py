from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    img = models.ImageField(upload_to='img')

    def __str__(self) -> str:
        return self.img.url


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField(default=10)
    active = models.BooleanField(default=True)
    on_menu = models.BooleanField(default=True)
    megamenu = models.BooleanField(default=False)

    class Meta:
        unique_together = ('slug', 'parent',)    #evitar duplicações
        verbose_name_plural = "categories"

    def __str__(self):                           
       return self.name

    def get_cat_list(self):
        category_path = []
        current_category = self
        while current_category:
            category_path.insert(0, current_category.slug)
            current_category = current_category.parent
        return category_path


class Tag(models.Model):
    tagname = models.CharField(max_length=20)

    def __str__(self):
        return self.tagname


class Post(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.DO_NOTHING)
    content = models.TextField()
    order = models.IntegerField(default=10)
    # content = models.HTMLField('Content')
    summary = models.CharField(max_length=1000, null=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True)
    image = models.ManyToManyField(Image, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.IntegerField(default=0)
    metadescription = models.CharField(max_length=300, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Template(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.name
