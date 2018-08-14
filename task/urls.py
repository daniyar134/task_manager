from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from task.views import TaskView, ProjectView, CommentView, DescriptionView


router = SimpleRouter(trailing_slash=False)
router.register('task', TaskView, base_name='task')
router.register('project', ProjectView, base_name='project')
router.register('comment', CommentView, base_name='comment')
router.register('description', DescriptionView, base_name='description')

urlpatterns = router.urls