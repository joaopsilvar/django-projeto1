from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 100


class RecipeAPIV2List(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination

    # def get(self,request):
    #     recipes = Recipe.objects.all()[:10]
    #     serializer = RecipeSerializer(
    #         instance=recipes,
    #         many=True,
    #         context={'request':request}
    #     )
    #     return Response(serializer.data)
    
    # def post(self,request):
    #     serializer = RecipeSerializer(
    #         data=request.data,
    #         context={'request':request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(
    #         author_id=1,
    #         category_id=1,
    #     )
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )

class RecipeAPIV2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.filter()
    serializer_class = RecipeSerializer


    # def get_recipe(self,pk):
    #     return get_object_or_404(
    #         Recipe.objects.filter(),
    #         pk=pk
    #     )
    
    # def get(self,request,pk):
    #     recipe = self.get_recipe(pk)
    #     if request.method == 'GET':
    #         serializer = RecipeSerializer(
    #             instance=recipe,
    #             many=False,
    #             context={'request':request}
    #     )
    #     return Response(serializer.data)
    
    # def patch(self,request,pk):
    #     recipe = self.get_recipe(pk)
    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         data=request.data,
    #         many=False,
    #         partial=True,
    #         context={'request':request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def delete(self,request,pk):
    #     recipe = self.get_recipe(pk)
    #     recipe.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
