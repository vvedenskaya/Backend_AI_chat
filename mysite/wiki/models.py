from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

class Document(models.Model):
    title_doc = models.CharField(max_length=255)

    def __str__(self):
        return self.title_doc