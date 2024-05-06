from unittest import TestCase
from utils.pagination import make_pagination_range, make_pagination
from recipes.tests.test_recipe_base import RecipeTestBase
from django.urls import reverse
from unittest.mock import patch
from recipes.models import Recipe
from django.http import HttpRequest


class PaginationTest(RecipeTestBase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        # Current page = 1 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 2 - Middle Page = 2
        # Here change page
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_if_the_pagination_is_correct_with_9_recipes(self):
        for item in range(15):
            recipes = self.make_recipe(author_data={'first_name': f'test_pagination_author{item}',
                                                    'username': f'test_pagination_username{item}'},
                                       slug=f'recipe-slug-for-no-defaults{
                                           item}',
                                       )
            recipes.full_clean()
            recipes.save()

        url = reverse('recipes:home')
        response = self.client.get(f'{url}?page=1')
        self.assertEqual(len(response.context['recipes']), 9)

    def test_if_the_pagination_is_correct(self):
        for item in range(8):
            recipes = self.make_recipe(author_data={'first_name': f'test_pagination_author{item}',
                                                    'username': f'test_pagination_username{item}'},
                                       slug=f'recipe-slug-for-no-defaults{
                                           item}',
                                       )
            recipes.full_clean()
            recipes.save()

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes_full = response.context['recipes']
            paginator = recipes_full.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_make_pagination_uses_page_1_if_page_query_is_invalid(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_pagination_uses_page_1_if_page_query_is_invalid(self):
        recipe = Recipe.objects.all()
        request = HttpRequest()
        request.GET['page'] = 'ABC'

        page_obj, pagination_range = make_pagination(request, recipe, 2)

        self.assertEqual(pagination_range['current_page'], 1)
