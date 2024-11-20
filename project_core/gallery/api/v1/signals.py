from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ...models import *


@receiver(post_save, sender=PictureLike)
def increment_counted_like(sender, instance, created, **kwargs):
    if created:
        picture_post = instance.picture_post
        picture_post.counted_likes += 1
        picture_post.save()


@receiver(post_delete, sender=PictureLike)
def decrement_counted_like(sender, instance, **kwargs):
    picture_post = instance.picture_post
    picture_post.counted_likes -= 1
    picture_post.save()


@receiver(post_save, sender=Dislike)
def increment_counted_dislike(sender, instance, created, **kwargs):
    if created:
        picture_post = instance.picture_post
        picture_post.counted_likes -= 1
        picture_post.save()

@receiver(post_delete, sender=Dislike)
def decrement_counted_dislike(sender, instance, **kwargs):
    picture_post = instance.picture_post
    picture_post.counted_likes += 1
    picture_post.save()


@receiver(post_save, sender=Save)
def increment_counted_save(sender, instance, created, **kwargs):
    if created:
        picture_post = instance.picture_post
        picture_post.counted_save += 1
        picture_post.save()


@receiver(post_delete, sender=Save)
def decrement_counted_save(sender, instance, **kwargs):
    picture_post = instance.picture_post
    picture_post.counted_save -= 1
    picture_post.save()



@receiver(post_save, sender=Share)
def increment_counted_share(sender, instance, created, **kwargs):
    if created:
        picture_post = instance.picture_post
        picture_post.counted_share += 1
        picture_post.save()

