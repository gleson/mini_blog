from django.db import models

class Catechism(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=240)
    text = models.TextField()
    related = models.CharField(max_length=60)
    
    def __str__(self):
        return f'{self.number} {self.text[:20]}'
