from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255, primary_key=True, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails", default="placeholder.jpg")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, verbose_name="Active")
    featured = models.BooleanField(default=False, verbose_name="Featured")
    tags = models.ManyToManyField(Tag, blank=True)
    meta_tags = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="comma seperated tags used for SEO ",
    )
    meta_description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="meta description used for SEO (max 170 characters)",
    )

    def __str__(self):
        return self.title

    def meta_tags_list(self):
        if self.meta_tags:
            return self.meta_tags.split(",")
        else:
            return None

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.title)
            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                slug = slugify(self.title) + "-" + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"slug": self.slug})
