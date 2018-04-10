from django.contrib import admin

# Register your models here.
from fractals.models import Configuration, Result

admin.site.register(Configuration)
admin.site.register(Result)
