from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from ..serializers import RecipesSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.all()[:10]
    serializer = RecipesSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view()
def recipe_api_detail(request,pk):
    recipe = get_object_or_404(
        Recipe.objects.filter(),
        pk=pk
    )
    serializer = RecipesSerializer(instance=recipe, many=False)
    return Response(serializer.data)