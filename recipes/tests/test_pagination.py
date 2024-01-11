from django.urls import resolve, reverse
from recipes import views
from unittest.mock import patch

from .test_recipe_base import RecipeTestBase


class RecipePaginationTest(RecipeTestBase):
    def test_recipe_pagination_home_view(self):
        import recipes
        for i in range(9):
            self.make_recipe(
                slug= f'slug-{i}', title=f'title{i}', author_data={'username': f'one{i}'}
            )

        with patch('recipes.views.PER_PAGE', new=3):
            search_url = reverse('recipes:search')
            response = self.client.get(f'{search_url}?q=title')
            recipes = response.context['recipes']
            paginator = recipes.paginator


            self.assertEqual(paginator.num_pages,3)
            self.assertEqual(len(paginator.get_page(1)),3)
            
