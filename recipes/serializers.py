from rest_framework import serializers
from .models import Category, Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=65)


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField(method_name='any_method_name')
    category = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset= Tag.objects.all(),
        many=True
    )

    tag_objects = TagSerializer(
        many=True, source='tags'
    ) 

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'