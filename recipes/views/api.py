from recipes.models import Recipe
from ..serializers import RecipeSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from ..permissions import IsOwner
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 10


class RecipeAPIV2Viewset(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk=self.kwargs.get('pk','')
        obj = get_object_or_404(
            self.queryset(),
            pk=pk
        )
        self.check_object_permissions(self.request, obj)
        return obj
    
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
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return[IsOwner()]
        return super().get_permissions()
    
    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )