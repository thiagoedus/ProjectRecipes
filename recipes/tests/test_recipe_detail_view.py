from unittest import skip

from recipes.tests.test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes.views import site


class RecipeDetailViewsTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertIs(view.func.view_class, site.RecipeDetail)

    def test_recipe_detail_view_return_statuscode_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is published False dont show"""
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_must_be_the_same_as_selected(self):
        recipe = self.make_recipe()

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.id}))

        self.assertEqual(response.status_code, 200)
