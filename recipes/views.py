
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, Http404
from django.db.models import Q
from recipes.models import Recipe, Category
from utils.pagination import make_pagination
import os
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def theory(request, *args, **kwargs):
    return render(request, 'recipes/pages/theory.html')


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)

        qs = qs.select_related('author', 'category')

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


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_args):

        recipes = self.get_context_data()['recipes'].object_list.values()
        return JsonResponse(
            list(recipes),
            safe=False
        )


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


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):

        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']

        return JsonResponse(
            recipe_dict,
            safe=False
        )

# def recipe(request, id):
#     recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

#     return render(request, 'recipes/pages/recipe-view.html', context={
#         'recipe': recipe,
#         'is_detail_page': True,
#     })
