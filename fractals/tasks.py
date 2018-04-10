import os
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile

from celery import shared_task
from fractals.models import Result


@shared_task
def create_fractal(result_id):
    result = Result.objects.get(id=result_id)
    configuration = result.configuration

    filename = f'{configuration.hash}.png'
    filename_with_path = f'{settings.BASE_DIR}/{filename}'
    call_ = subprocess.run(
        [
            'python', 'fractals/fractal.py', 'julia',
            f'{configuration.real_constant} {float_to_str_with_sign(configuration.imaginary_constant)} j ',
            '-d', str(configuration.depth),
            '-s', f'{configuration.resolution}x{configuration.resolution}',
            '-o', filename_with_path,
            '-m', configuration.colormap
        ]
    )
    if call_.returncode == 0:
        with open(filename_with_path, 'rb') as f:
            image_data = f.read()
        content_file = ContentFile(image_data)
        result.set_result(content_file)
        os.remove(filename_with_path)


def float_to_str_with_sign(value):
    sign = '+' if value >= 0 else ''
    return f'{sign}{value}'
