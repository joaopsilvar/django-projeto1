from django.urls import path
from .views import site,api

app_name = 'recipes'

urlpatterns = [
    path('',site.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search/', site.RecipeListViewSearch.as_view(), name="search"),
    path('recipes/category/<int:category_id>/',site.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/<int:pk>/',site.RecipeDetail.as_view(), name="recipe"),
    path('recipes/api/v1/',site.RecipeListViewHomeApi.as_view(), name="recipes_api_v1"),
    path('recipes/api/v1/<int:pk>/',site.RecipeDetailApi.as_view(), name="recipes_api_v1_detail"),
    path('recipes/api/v2/',api.RecipeAPIV2List.as_view(), name="recipes_api_v2"),
    path('recipes/api/v2/<int:pk>/',api.RecipeAPIV2Detail.as_view(), name="recipes_api_v2_detail"),

]
