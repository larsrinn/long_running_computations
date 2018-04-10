from django.contrib import admin

# Register your models here.
from fractals.models import Configuration, Computation

admin.site.register(Configuration)
admin.site.register(Computation)
