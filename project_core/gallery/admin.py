from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(MidjernyImage)
class MidjernyImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'image_webp', 'image_original', 'counted_likes', 'counted_save',
                    'created_date', 'updated_date')
    search_fields = ('title', 'publisher')
    list_filter = ('title', 'publisher')
    ordering = ('-created_date',)
    readonly_fields = ('counted_likes', 'counted_save')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Size_picture)
class Size_pictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')
    search_fields = ('name',)

@admin.register(PictureLike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'picture_post')
    search_fields = ('user__user__username', 'picture_post__title')

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'picture_post')
    search_fields = ('user__user__username', 'picture_post__title')
    list_filter = ('user', )


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'picture_post')
    search_fields = ('user__user__username', 'picture_post__title')
    list_filter = ('user', )
