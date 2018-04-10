from django import forms

from fractals.models import Configuration
from fractals.tasks import create_fractal


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['image']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        create_fractal.delay(instance.id)
        return instance
