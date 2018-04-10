from django import forms

from fractals.models import Configuration
from fractals.tasks import create_fractal


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['image', 'computing']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        result = instance.set_computing()
        create_fractal.delay(result.id)
        return instance
