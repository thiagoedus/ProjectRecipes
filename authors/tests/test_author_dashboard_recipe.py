from recipes.tests.test_recipe_base import RecipeTestBase
from django.test import TestCase
from django.urls import reverse
from recipes.models import User


class AuthorDashboardRecipe(RecipeTestBase):

    def setUp(self) -> None:
        self.recipe = self.make_recipe(is_published=False)
        self.client.login(username=self.recipe.author.username,
                          password='123456')
        return super().setUp()

    def test_author_recipe_detail_get_and_post_successfully(self):
        response = self.client.get(reverse('authors:dashboard_recipe_edit', kwargs={
                                   'id': self.recipe.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_author_recipe_detail_not_recipe_is_404(self):
        response = self.client.get(
            reverse('authors:dashboard_recipe_edit', kwargs={'id': 1000}), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_author_recipe_user_form_edit_if_not_correct_returns_404(self):
        self.make_author(username='username2',
                         password='1234567')

        self.client.login(username='username2',
                          password='1234567')

        response = self.client.get(reverse('authors:dashboard_recipe_edit', kwargs={
                                   'id': self.recipe.id}))

        self.assertEqual(response.status_code, 404)

    def test_author_recipe_form_edit_template_used_form_is_correct(self):
        response = self.client.get(reverse('authors:dashboard_recipe_edit', kwargs={
                                   'id': self.recipe.id}), follow=True)
        self.assertTemplateUsed(
            response, 'global/partials/form.html')
