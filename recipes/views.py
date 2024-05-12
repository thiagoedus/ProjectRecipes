from django.db.models.query import QuerySet
from django.shortcuts import get_list_or_404, get_object_or_404, render, Http404
from django.db.models import Q
from recipes.models import Recipe, Category
from utils.pagination import make_pagination
import os
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context_data.get('recipes'), PER_PAGE)
        context_data.update(
            {'recipes': page_obj, 'pagination_range': pagination_range})
        return context_data


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if not Category.objects.filter(id=self.kwargs.get('category_id')).first():
            raise Http404()
        qs = qs.filter(category__id=self.kwargs.get('category_id'))
        return qs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        first_recipe = context_data.get('recipes')[0]
        context_data['title'] = f'{first_recipe.category.name} - Category | '
        return context_data


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_search_therm(self):
        search_therm = self.request.GET.get('q', '').strip()

        if not search_therm:
            raise Http404()

        return search_therm

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            Q(
                Q(title__icontains=self.get_search_therm()) |
                Q(description__icontains=self.get_search_therm()),
            ),
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        search_therm = self.get_search_therm()

        context_data.update(
            {'page_title': f'Search for "{ search_therm }" |',
             'search_term': search_therm,
             'additional_url_query': f'&q={search_therm}'}
        )
        return context_data


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data.update(
            {'is_detail_page': True}
        )
        return context_data

# def recipe(request, id):
#     recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

#     return render(request, 'recipes/pages/recipe-view.html', context={
#         'recipe': recipe,
#         'is_detail_page': True,
#     })
