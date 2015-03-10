# -*- coding: utf-8 -*-
from django import forms

from places_core.forms import BootstrapBaseForm

from .models import SocialProject, TaskGroup, Task


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


class TaskGroupForm(forms.ModelForm, BootstrapBaseForm):
    """ Tworzenie oraz edycja grup zadań. """
    class Meta:
        model = TaskGroup
        fields = ('name', 'description', 'project', 'creator',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'creator': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }


class TaskForm(forms.ModelForm, BootstrapBaseForm):
    """ Tworzenie/edycja zadania. """
    class Meta:
        model = Task
        exclude = ('participants', 'is_done',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'creator': forms.HiddenInput(),
            'group': forms.HiddenInput(),
        }
