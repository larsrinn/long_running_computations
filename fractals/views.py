from django.http import JsonResponse
from django.urls import reverse
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

    def get_context_data(self, **kwargs):
        kwargs['computing'] = self.object.computing
        if self.object.computing:
            kwargs['polling_url'] = reverse('configuration-computing', args=[self.object.pk])
        return super().get_context_data(**kwargs)


class ConfigurationList(ListView):
    model = Configuration
    template_name = 'fractals/configuration_list.html'


def computation_is_computing(request, pk):
    configuration = Configuration.objects.get(pk=pk)
    return JsonResponse({
        'computing': configuration.computing
    })
