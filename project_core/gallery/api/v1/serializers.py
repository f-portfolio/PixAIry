import zipfile
from rest_framework import serializers
from datetime import timezone
from gallery.models import *
from rest_framework import serializers, permissions
from accounts.models import Profile
from ...models import *
import os


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'image']


class MidjernyImageserializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if ('request' in self.context
            and self.context['request'].user.is_authenticated  
            and self.context['request'].user.is_verified  
            and self.context['request'].user.is_staff
            and self.context['request'].user.is_supervisor == False
                and self.context['request'].user.is_superuser == False):
            self.Meta.read_only_fields = [
                'publisher', 'image_webp', 'counted_likes', 'counted_save',]

        elif ('request' in self.context
              and self.context['request'].user.is_authenticated
              and self.context['request'].user.is_verified
              and (self.context['request'].user.is_supervisor or self.context['request'].user.is_superuser)):
            self.Meta.read_only_fields = [
                'publisher', 'image_webp', 'counted_likes', 'counted_save', ]

        else:
            self.Meta.read_only_fields = ['id','site_name', 'title', 'midjerny_id', 'category', 'size_picture', 'description', 'publisher', 'image_webp', 'image_original',
                                          'tags', 'counted_likes', 'counted_save', 'created_date', 'updated_date',
                                          ]

    class Meta:
        model = MidjernyImage
        fields = ['id','site_name', 'title', 'publisher', 'description', 'category', 'size_picture', 
                  'midjerny_id', 'image_webp', 'image_original', 'tags',
                  'counted_likes', 'counted_save', 'created_date', 'updated_date']

    def validate_tags(self, value):
        if len(value) > 7:
            raise serializers.ValidationError(
                "The number of tags should not exceed 7.")
        return value


class MidjernyImageBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = MidjernyImage
        fields = ['title', 'description', 'midjerny_id', 'category', 'tags', 'size_picture']

    def validate_tags(self, value):
        if len(value) > 7:  
            raise serializers.ValidationError("The number of tags should not exceed 7.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['publisher'] = request.user.profile  
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.midjerny_id = validated_data.get('midjerny_id', instance.midjerny_id)
        instance.category = validated_data.get('category', instance.category)
        instance.tags.set(validated_data.get('tags', instance.tags.all()))
        instance.size_picture.set(validated_data.get('size_picture', instance.size_picture.all()))
        instance.save()
        return instance


class MidjernyImagePictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = MidjernyImage
        fields = [ 'title','image_original']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['publisher'] = {
            'id': instance.publisher.id,
            'name': instance.publisher.user.username  
        }
        return rep


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'user_adder', 'created_date', 'updated_date']
        read_only_fields = ['user_adder',]
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user_adder'] = request.user.profile
        return super().create(validated_data)

class Size_pictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size_picture
        fields = ['id', 'name', 'value']


class UploadImagesAndExcelSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True)  
    images_zip = serializers.FileField(write_only=True)  
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    
    def create(self, validated_data):
        file = validated_data.pop('file')
        images_zip = validated_data.pop('images_zip')
        category = validated_data.pop('category')
        
        zip_path = os.path.join('path/to/save', images_zip.name)  
        with open(zip_path, 'wb') as zip_file:
            zip_file.write(images_zip.read())

        extract_path = 'path/to/extracted/images'  
        os.makedirs(extract_path, exist_ok=True)  
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        return validated_data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureLike
        fields = ['id', 'user', 'picture_post',]
        read_only_fields = ['user']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['user'] = ProfileSerializer(
            instance.user, context={'request': request}).data
        rep['picture_post'] = MidjernyImageserializer(
            instance.picture_post, context={'request': request}).data
        return rep

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user.profile
        return super().create(validated_data)
    
class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['id', 'user', 'picture_post',]
        read_only_fields = ['user']

    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        rep['user'] = ProfileSerializer(instance.user, context={'request':request}).data
        rep['picture_post'] = MidjernyImageserializer(instance.picture_post, context={'request':request}).data
        return rep

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user.profile
        return super().create(validated_data)

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = ['id', 'user', 'picture_post',]
        read_only_fields = ['user']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['user'] = ProfileSerializer(
            instance.user, context={'request': request}).data
        rep['picture_post'] = MidjernyImageserializer(
            instance.picture_post, context={'request': request}).data
        return rep

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user.profile
        return super().create(validated_data)
