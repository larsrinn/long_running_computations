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

    @property
    def latest_configuration_computation(self):
        return self.computations.last()

    @property
    def computing(self):
        return self.latest_configuration_computation.computing

    @property
    def image(self):
        return self.latest_configuration_computation.image

    @property
    def hash(self):
        self_dict = model_to_dict(self)
        self_dict.pop('id')
        hash_object = hashlib.md5(json.dumps(self_dict).encode('utf-8'))
        return hash_object.hexdigest()

    def get_absolute_url(self):
        return reverse('configuration-update', args=[self.id])

    def set_computing(self):
        return Computation.objects.create(
            configuration=self,
            computing=True,
            image=self.latest_configuration_computation.image,
        )


class Computation(models.Model):
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, related_name='computations')
    image = models.FileField(blank=True, null=True)
    computing = models.BooleanField()

    def set_result(self, content_file):
        self.image.save(name='fractal.png', content=content_file)  # django avoids duplicate names automatically
        self.computing = False
        self.save()
