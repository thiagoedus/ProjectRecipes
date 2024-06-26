from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)

@api_view(http_method_names=['get', 'post'])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
    recipe = recipe.prefetch_related('category', 'author')
    serializer = RecipeSerializer(instance=recipe, many=False)
    return Response(serializer.data)

    # recipe = Recipe.objects.get_published().filter(pk=id).first()

    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         "detail": "ERRO"
    #     }, status=status.HTTP_418_IM_A_TEAPOT)