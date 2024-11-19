from .views import UploadImagesAndExcelViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

from . import views
from django.urls import path, include

app_name = 'api-v1'

urlpatterns = [
    path('show_post/',ImageModelViewSet.as_view({'get': 'list', 'post': 'create'}), name="post-list"),
    path('show_post/<int:pk>/', ImageModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="post-detail"),

    path('picture_posts_edit_body/<int:pk>/', MidjernyImageEditBodyModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name='picturepost-detail-update-body'),
    path('picture_posts_edit_image/<int:pk>/', MidjernyImageEditPictureModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name='picturepost-detail-update-image'),


    path('upload/', UploadImagesAndExcelViewSet.as_view({'get': 'list', 'post': 'create'}), name='upload_images'),

    path('like_picture/',LikeModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='like-picture'),
    path('like_picture/<int:pk>/',LikeModelViewSet.as_view({'get': 'retrieve'}), name="like-picture"),

    path('dislike_picture/', DisLikeModelViewSet.as_view({'get':'list', 'post':'create'}), name='dislike-picture'),
    path('dislike_picture/<int:pk>/', DisLikeModelViewSet.as_view({'get':'retrieve'}), name="dislike-picture"),


    path('save_picture/',SaveModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='save-picture'),
    path('save_picture/<int:pk>/', SaveModelViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name="save-picture"),

]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import UploadImagesAndExcelViewSet

# router = DefaultRouter()
# router.register(r'upload', UploadImagesAndExcelViewSet, basename='upload')

# urlpatterns = [
#     path(' ', include(router.urls)),
# ]
