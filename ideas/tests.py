# -*- coding: utf-8 -*-
from django.test import TestCase

from .models import Idea

class IdeaListTestCase(TestCase):
    """ Test filtered list view for all ideas. """
    fixtures = ['fixtures/ideas.json',]

    def test_that_ideas_are_loaded(self):
        self.assertTrue(Idea.objects.count())
