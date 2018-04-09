from django.views.generic import CreateView, ListView, UpdateView

from fractals.forms import ConfigurationForm
from fractals.models import Configuration


class ConfigurationCreate(CreateView):
    form_class = ConfigurationForm
    template_name = 'fractals/configuration_form.html'


class ConfigurationUpdate(UpdateView):
    model = Configuration
    form_class = ConfigurationForm
    template_name = 'fractals/configuration_form.html'


class ConfigurationList(ListView):
    model = Configuration
    template_name = 'fractals/configuration_list.html'
