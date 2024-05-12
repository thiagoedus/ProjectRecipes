from recipes.tests.test_recipe_base import RecipeTestBase
from django.test import TestCase
from django.urls import reverse
from recipes.models import User

class AuthorDashboardRecipe(RecipeTestBase):
    def setUp(self):
        return

    def test_recipe_detail_get_and_post_successfully(self):
        recipe = self.make_recipe()
        self.client.login(username=recipe.author.username, password=recipe.author.password)

        response = self.client.get(reverse('authors:dashboard_recipe_edit', kwargs={'id':recipe.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_not_recipe_is_404(self):
        author = self.make_author()
        self.client.login(username=author.username, password=author.password)

        response = self.client.get(reverse('authors:dashboard_recipe_edit', kwargs={'id':1000}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_template_used_form_is_correct(self):
        recipe = self.make_recipe()
        self.client.login(username=recipe.author.username, password=recipe.author.password)

        response = self.client.get(reverse('authors:dashboard_recipe_edit', kwargs={'id':recipe.id}), follow=True)
        self.assertTemplateUsed(response, 'global/partials/form.html')



    
