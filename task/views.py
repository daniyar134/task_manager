from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
import django_filters
from rest_framework.permissions import IsAuthenticated

from task.models import Task, Description, Comment, Project
from task.serializers import TaskSerializer, DescriptionSerializer, CommentSerializer, ProjectSerializer
from task.filters import TaskFilter


class TaskView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
               mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.get_queryset()
    filter_class = TaskFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)


class DescriptionView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
               mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = DescriptionSerializer
    queryset = Description.objects.get_queryset()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)


class CommentView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
               mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.get_queryset()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)


class ProjectView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
               mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.get_queryset()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)


