# -*- coding: utf-8 -*-
from django import forms

from places_core.forms import BootstrapBaseForm

from .models import SocialProject


class CreateProjectForm(forms.ModelForm, BootstrapBaseForm):
    """ Tworzenie nowych projektów - część danych jest autouzupełniana. """
    class Meta:
        model = SocialProject
        fields = ('name', 'description', 'creator', 'location',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'creator': forms.HiddenInput(),
            'location': forms.HiddenInput(),
        }


class UpdateProjectForm(forms.ModelForm, BootstrapBaseForm):
    """ Edycja istniejących projektów ma inny zestaw pól. """
    class Meta:
        model = SocialProject
        fields = ('name', 'description', 'is_done',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
