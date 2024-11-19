from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
import os
import zipfile
from django.core.cache import cache
from rest_framework.parsers import MultiPartParser, FileUploadParser
import openpyxl
from PIL import Image
import shutil
from django.conf import settings
from accounts.models import Profile
import pandas as pd
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from ...models import *
from .permissions import *
from .paginations import *
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ImageModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsAdminUser, IsOwnerOrSupervisor]
    serializer_class = MidjernyImageserializer
    queryset = MidjernyImage.objects.all()
    list_display = ('title', 'category',
                    'midjerny_id,' 'publisher', 'created_date')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site_name', 'title', 'tags', 'category']
    search_fields = ['site_name', 'title', 'midjerny_id', 'category']
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        # serializer.save(publisher=profile)
        instance = serializer.save(publisher=profile)

        if instance.image_original:
            original_image_path = instance.image_original.path  
            
            base_name, _ = os.path.splitext(original_image_path)
            webp_image_path = base_name.replace(
                'original', 'webp') + '.webp' 
            
            os.makedirs(os.path.dirname(webp_image_path), exist_ok=True)

            with Image.open(original_image_path) as img:
                img.save(webp_image_path, 'WEBP', quality=75)

            instance.image_webp = webp_image_path
            instance.save()

class MidjernyImageEditBodyModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsOwnerOrSupervisor]
    queryset = MidjernyImage.objects.all()
    serializer_class = MidjernyImageBodySerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site_name', 'category', 'tags', 'publisher']
    search_fields = ['title', 'description', 'midjerny_id',
                     'publisher__user__username', 'tags__name']

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Image uploaded and processing started",
            "image": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "The object was successfully updated.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Image deleted successfully."
        }, status=status.HTTP_200_OK)

class MidjernyImageEditPictureModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsOwnerOrSupervisor]
    queryset = MidjernyImage.objects.all()
    serializer_class = MidjernyImagePictureSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site_name', 'publisher', 'category']
    search_fields = ['title', 'midjerny_id', 'publisher__user__username']
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Image uploaded and processing started",
            "image": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance.image_original:
            self.convert_to_webp(instance)
        return Response({
            "message": "The object was successfully updated.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def convert_to_webp(self, instance):
        original_image_path = instance.image_original.path  
        base_name, _ = os.path.splitext(original_image_path)
        webp_image_name = os.path.basename(
            base_name) + '.webp'  
        webp_directory = r'C:\Users\Webhouse\Desktop\midjerny_monolotic\media\images\webp'
        webp_image_path = os.path.join(webp_directory, webp_image_name)

        os.makedirs(webp_directory, exist_ok=True)

        if not os.path.exists(webp_image_path):
            with Image.open(original_image_path) as img:
                img.save(webp_image_path, 'WEBP', quality=75)

        instance.image_webp.name = os.path.join(
            'images/webp', webp_image_name) 
        instance.save(update_fields=['image_webp'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Image deleted successfully."
        }, status=status.HTTP_200_OK)



class UploadImagesAndExcelViewSet(viewsets.ModelViewSet):
    queryset = MidjernyImage.objects.all()
    serializer_class = UploadImagesAndExcelSerializer
    parser_classes = (MultiPartParser,)
    pagination_class = CustomPageNumberPagination

    def create(self, request, *args, **kwargs):
        excel_file = request.FILES.get('file')
        images_zip = request.FILES.get('images_zip')
        category = request.data.get('category')

        if not excel_file or not images_zip or not category:
            return Response({'error': 'Excel file, images zip, and category are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_excel(excel_file)
            # print("DataFrame loaded successfully:", df)
            print("DataFrame loaded successfully:") 
        except Exception as e:
            return Response({'error': f'Error reading excel file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        original_dir = os.path.join(settings.MEDIA_ROOT, 'images/original/')
        webp_dir = os.path.join(settings.MEDIA_ROOT, 'images/webp/')
        os.makedirs(original_dir, exist_ok=True)
        os.makedirs(webp_dir, exist_ok=True)

        extract_path = os.path.join(settings.MEDIA_ROOT, 'images/extracted/')
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(images_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        extracted_files = os.listdir(extract_path)
        print("Extracted files:", extracted_files)

        for index, row in df.iterrows():
            title = row.get('title')
            description = row.get('description')
            midjerny_id = row.get('midjerny_id')
            tags = row.get('tags', '')
            size_picture_names = row.get('size_picture', '')
            image_name_original = row.get('image_original')
            category_obj = Category.objects.get(pk=category)

            if isinstance(image_name_original, float) or not image_name_original:
                print(f"Skipping row {index} due to invalid image name.")
                continue  
            
            image_name_original = str(image_name_original).strip()
            
            image_path_original = os.path.join(
                original_dir, image_name_original)

            image_found = False
            for folder in extracted_files:
                src_image_path = os.path.join(
                    extract_path, folder, image_name_original)
                if os.path.isfile(src_image_path):
                    
                    with open(image_path_original, 'wb+') as destination:
                        with open(src_image_path, 'rb') as src_file:
                            destination.write(src_file.read())

                    
                    webp_image_path = os.path.join(
                        webp_dir, os.path.splitext(image_name_original)[0] + '.webp')
                    with Image.open(image_path_original) as img:
                        img.save(webp_image_path, 'WEBP')

                    print(
                        f"Image {image_name_original} processed successfully from folder {folder}.")
                    image_found = True
                    break  
                
            if not image_found:
                print(
                    f'Image {image_name_original} not found in any extracted folder.')
                continue  
            
            try:
                admin_profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                return Response({'error': 'Profile does not exist for the logged-in user.'}, status=status.HTTP_404_NOT_FOUND)

            tags_list = tags.split(",") if tags else []
            tag_objects = [Tag.objects.get_or_create(
                name=tag.strip())[0] for tag in tags_list]

            size_picture_list = size_picture_names.split(
                ",") if size_picture_names else []
            size_picture_objects = [Size_picture.objects.get_or_create(
                name=size_name.strip())[0] for size_name in size_picture_list]

            midjerny_image = MidjernyImage.objects.create(
                title=title,
                description=description,
                midjerny_id=midjerny_id,
                publisher=admin_profile,  
                image_original=image_path_original,
                image_webp=webp_image_path,
                counted_likes=0,
                counted_save=0,
                category=category_obj,
            )
            midjerny_image.tags.set(tag_objects)
            midjerny_image.size_picture.set(size_picture_objects)

        shutil.rmtree(extract_path)
        print(f"Removed extracted folder: {extract_path}")

        return Response({'status': 'success', 'message': 'Images processed and saved successfully.'})


class LikeModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = PictureLike.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'picture_post']
    search_fields = ['user__user__username', 'picture_post__title',]
    pagination_class = CustomPageNumberPagination


class DisLikeModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DisLikeSerializer
    queryset = Dislike.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'picture_post']
    search_fields = ['user__user__username', 'picture_post__title',]


class SaveModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SaveSerializer
    queryset = Save.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'picture_post']
    search_fields = ['user__user__username', 'picture_post__title',]
    