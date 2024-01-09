from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipePaginationTest(RecipeTestBase):
    def test_recipe_pagination_home_view(self):
        for i in range(20):
            self.make_recipe(
                slug= f'slug-{i}', title=f'title{i}', author_data={'username': f'one{i}'}
            )
        search_url = reverse('recipes:search')
        response = self.client.get(f'{search_url}?q=title')
        self.assertEqual(len(response.context['recipes']),9)
