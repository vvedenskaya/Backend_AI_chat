from django.db import models

class Article(models.Model):
    train = models.TextField()
    text = models.TextField()




    def __str__(self):
        return self.title


