from recipes.models import Recipe
from ..serializers import RecipeSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 10


class RecipeAPIV2Viewset(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    
    def get_serializer_class(self):
        return super().get_serializer_class()
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example"] = 'esse é o contexto'
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id','')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs