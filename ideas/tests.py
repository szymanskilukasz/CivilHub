# -*- coding: utf-8 -*-
from django.test import TestCase

from .models import Category, Idea


class IdeaListTestCase(TestCase):
    """ Test filtered list view for all ideas. """
    fixtures = ['fixtures/users.json',
                'fixtures/locations.json',
                'fixtures/ideas.json',]

    def test_that_ideas_are_loaded(self):
        self.assertTrue(Category.objects.count())
        self.assertTrue(Idea.objects.count())
