import subprocess

from django import forms
from django.conf import settings

from fractals.models import Configuration


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['image']

    def save(self, commit=True):
        create_fractal(self.instance)
        return super().save(commit=commit)


def create_fractal(configuration):
    filename = f'{configuration.hash}.png'
    call_ = subprocess.run(
        [
            'python', 'fractals/fractal.py', 'julia',
            f'{configuration.real_constant} {float_to_str_with_sign(configuration.imaginary_constant)} j ',
            '-d', str(configuration.depth),
            '-s', f'{configuration.resolution}x{configuration.resolution}',
            '-o', f'{settings.MEDIA_ROOT}/{filename}',
            '-m', configuration.colormap
        ]
    )
    if call_.returncode == 0:
        configuration.image = filename
        configuration.save()


def float_to_str_with_sign(value):
    sign = '+' if value >= 0 else ''
    return f'{sign}{value}'
