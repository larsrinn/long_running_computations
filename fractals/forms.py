from django import forms

from fractals.models import Configuration
from fractals.tasks import create_fractal


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['image', 'computing']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.set_computing()  # can't do that in the task, because it might wait in the queue for a while
        create_fractal.delay(instance.id)
        return instance
