from django.urls import path
from .views import site,api
from rest_framework.routers import SimpleRouter

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register('recipes/api/v2',api.RecipeAPIV2Viewset,'recipes-api')

urlpatterns = [
    path('',site.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search/', site.RecipeListViewSearch.as_view(), name="search"),
    path('recipes/category/<int:category_id>/',site.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/<int:pk>/',site.RecipeDetail.as_view(), name="recipe"),
    path('recipes/api/v1/',site.RecipeListViewHomeApi.as_view(), name="recipes_api_v1"),
    path('recipes/api/v1/<int:pk>/',site.RecipeDetailApi.as_view(), name="recipes_api_v1_detail"),
]

urlpatterns+=recipe_api_v2_router.urls
