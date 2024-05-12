from unittest import skip

from recipes.tests.test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeCategoryViewsTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1000}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_return_statuscode_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is published False dont show"""
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_if_recipes_in_correct_category(self):
        name_category = 'category_test'
        recipe = self.make_recipe(category_data={'name': name_category})
        recipe.save()

        response = self.client.get(reverse('recipes:category', kwargs={
                                   'category_id': recipe.category.id}))

        self.assertIn(recipe.title, response.content.decode())
