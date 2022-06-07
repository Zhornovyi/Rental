from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def upload_location(instance, filename, **kwargs):
    file_path = f'estates/{str(instance.author.id)}/{str(instance.post_title)}-{filename}'
    return file_path


class EstatePost(models.Model):
    post_title = models.CharField(max_length=100, null=False, blank=True)
    description = models.TextField(max_length=5000, null=False, blank=True)

    city = models.CharField(max_length=120, null=False, blank=True)
    address = models.TextField(max_length=500, null=False, blank=True)
    price = models.IntegerField(default=0, null=False, blank=True)
    square_meters = models.IntegerField(default=0, null=False, blank=True)
    type = models.CharField(max_length=100, null=False, blank=True)
    floor = models.IntegerField(null=True, blank=True)

    proof_doc = models.FileField(upload_to=upload_location, null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    contracted = models.BooleanField(default=False, blank=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        db_table = "estates_posts"

    def __str__(self):
        return self.post_title


class EstateReview(models.Model):
    text = models.TextField(max_length=5000)
    rate = models.IntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    estate = models.ForeignKey(EstatePost, on_delete=models.CASCADE)

    class Meta:
        db_table = "estate_reviews "


@receiver(post_delete, sender=EstatePost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_estate_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.post_title)


pre_save.connect(pre_save_estate_post_receiever, sender=EstatePost)

