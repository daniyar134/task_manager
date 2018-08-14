import django_filters

from task.models import Task


class TaskFilter(django_filters.FilterSet):
    id = django_filters.Filter(name='id', lookup_expr='exact')
    name = django_filters.Filter(name='name', lookup_expr='icontains')
    maker = django_filters.Filter(name='maker', lookup_expr='exact')
    author = django_filters.Filter(name='author', lookup_expr='exact')
    description = django_filters.Filter(name='description__text', lookup_expr='icontains')
    project = django_filters.Filter(name='project', lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['id', 'name', 'author', 'maker', 'author', 'description', 'project']