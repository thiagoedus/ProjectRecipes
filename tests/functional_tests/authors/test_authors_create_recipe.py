import pytest

from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.mark.functional_test
class AuthorsDashBoardRecipeTest(AuthorsBaseTest):
    recipe_title = 'Test Recipe Title'