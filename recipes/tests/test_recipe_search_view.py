from unittest import skip

from recipes.tests.test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views

class RecipeSearchViewsTest(RecipeTestBase):


    def test_recipe_search_users_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_therm(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Teste'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='recipe_test_one',
            title=title,
            author_data={'username':'test_one'}
        )

        recipe2 = self.make_recipe(
            slug='recipe_test_two',
            title=title2,
            author_data={'username':'test_two'}
        )

        url_search = reverse('recipes:search')
        response1 = self.client.get(f'{url_search}?q={title}')
        response2 = self.client.get(f'{url_search}?q={title2}')
        response_both = self.client.get(f'{url_search}?q=this')
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])


    def test_recipe_search_can_find_recipe_by_description(self):
        description = 'This is recipe description one'
        description2 = 'This is recipe description two'

        recipe1 = self.make_recipe(
            slug='recipe_test_one',
            title = 'This is recipe one',
            description=description,
            author_data={'username':'test_one'}
        )

        recipe2 = self.make_recipe(
            slug='recipe_test_two',
            title = 'This is recipe two',
            description=description2,
            author_data={'username':'test_two'}
        )

        url_search = reverse('recipes:search')

        response1 = self.client.get(f'{url_search}?q={recipe1.title}')
        response2 = self.client.get(f'{url_search}?q={recipe2.title}')
        response_both = self.client.get(f'{url_search}?q=this')

        self.assertIn(
            recipe1.description,
            response1.content.decode('utf-8')
            )
        
        self.assertNotIn(
            recipe2.description,
            response1.content.decode('utf-8')
            ) 
        
        self.assertIn(
            recipe2.description,
            response2.content.decode('utf-8')
            )
        
        self.assertNotIn(
            recipe1.description,
            response2.content.decode('utf-8')
            ) 

        self.assertIn(
            recipe1.description,
            response_both.content.decode('utf-8')
            ) 
        
        self.assertIn(
            recipe2.description,
            response_both.content.decode('utf-8')
            ) 
        
        self.assertNotIn(
            'Not recipes found',
            response_both.content.decode('utf-8')
            ) 