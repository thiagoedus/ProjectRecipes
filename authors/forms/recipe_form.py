from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self._my_errors = defaultdict(list)

        add_attr(self.fields.get('title'), 'class', 'span-2')
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps',
                  'cover', 'category',)

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    # def clean(self, *args, **kwargs) {
    #     super_clean = super().clean(*args, **kwargs)

    #     return super_clean
    # }
