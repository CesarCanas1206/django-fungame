from django.db import models
from django_extensions.db.fields import AutoSlugField
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.


class Page(models.Model):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from="title", unique=True, db_index=True)
    content = RichTextField(verbose_name="Page Content")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:page", kwargs={"slug": self.slug})
