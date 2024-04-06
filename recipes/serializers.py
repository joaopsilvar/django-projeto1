from rest_framework import serializers
from .models import Recipe,Category
from authors.validators import AuthorRecipeValidator
import uuid
from django.utils.text import slugify

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title','description', 'author','category',
            'public', 'preparation','preparation_time',
            'preparation_time_unit','servings', 'servings_unit',
            'preparation_steps', 'cover'
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        read_only=True,
    )
    category = CategorySerializer(read_only=True)

    def get_preparation(self, recipe):
        return {
            'time' : recipe.preparation_time,
            'unit': recipe.preparation_time_unit
        }
    
    def validate(self,attrs):
        #no validated is request method is PATCH
        no_validated_fields = ['servings','preparation_time']
        for field in no_validated_fields:
            if self.instance is not None and attrs.get(field) is None:
                attrs[field] = getattr(self.instance,field)

        super_validate = super().validate(attrs)
        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError)
        return super_validate
