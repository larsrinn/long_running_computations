from django import forms

from fractals.models import Configuration
from fractals.tasks import create_fractal


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['image', 'computing']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.revoke_computing_computations()
        result = instance.set_computing()
        async_result = create_fractal.delay(result.id)
        result.task_id = async_result.id
        result.save()
        return instance
