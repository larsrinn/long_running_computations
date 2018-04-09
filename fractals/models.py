import hashlib
import json

from django.db import models
from django.forms import model_to_dict
from django.urls import reverse


class Configuration(models.Model):
    COLORMAP_CHOICES = [
        ('nipy_spectral', 'Nipy Spectral'),
        ('cubehelix', 'Cubehelix'),
        ('Oranges', 'Orange'),
        ('gnuplot', 'Gnuplot'),
        ('terrain', 'Terrain'),
        ('ocean', 'Ocean'),
    ]
    real_constant = models.FloatField(verbose_name='Real Constant',
                                      help_text='Real part of the constant used to define the julia set')
    imaginary_constant = models.FloatField(verbose_name='Imaginary Constant',
                                           help_text='Imaginary part of the constant used to define the julia set')
    depth = models.IntegerField(default=256, verbose_name='Iteration Depth')
    resolution = models.IntegerField(default=512, verbose_name='Resolution [px]',
                                     help_text='A squared image with the value as side length is created')
    colormap = models.CharField(max_length=20, choices=COLORMAP_CHOICES, default='nipy_spectral')
    image = models.FileField(blank=True, null=True, default='default.png')

    @property
    def hash(self):
        self_dict = model_to_dict(self)
        self_dict.pop('id')
        self_dict.pop('image')
        hash_object = hashlib.md5(json.dumps(self_dict).encode('utf-8'))
        return hash_object.hexdigest()

    def get_absolute_url(self):
        return reverse('configuration-update', args=[self.id])
