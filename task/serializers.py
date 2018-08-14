from rest_framework import serializers

from task.models import Task, Description, Comment, Project


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    description = DescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'author', 'maker', 'comment', 'status', 'project')