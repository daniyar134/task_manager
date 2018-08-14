from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from task.models import Task, Description, Comment, Project


class TestAuth(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('abc1234')
        self.user.save()

    def test_auth(self):
        data = {
            'username': 'test',
            'password': 'abc1234'
        }

        response = self.client.post('/api/token-auth/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['token'])


class TestCommon(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@localhost.localdomain')
        self.user.set_password('abc1234')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_common(self):
        # Создадим задачу
        data = {
            "name": "test_task",
            "status": Task.NEED,
            "author": self.user.id
        }
        response = self.client.post(reverse('task-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_id = response.json()['id']

        # Добавим описание к задаче
        response = self.client.post(reverse('description-list'), {'text': 'test_description', 'task': task_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Добавим комментарий к задаче
        response = self.client.post(reverse('comment-list'), {'text': 'test_comment', 'task': task_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Создадим проект и задачу назначим на него
        response = self.client.post(reverse('project-list'), {'name': 'test_project'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project_id = response.json()['id']

        response = self.client.patch(reverse('task-detail', kwargs={'pk': task_id}), {'project': project_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Изменим статус задачи и назначим исполнителя
        response = self.client.patch(reverse('task-detail', kwargs={'pk': task_id}),
                                     {'status': Task.PROGRESS, 'maker': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Получим детализацию задачи по id
        response = self.client.get(reverse('task-detail', kwargs={'pk': task_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test_task')
        self.assertEqual(response.json()['status'], Task.PROGRESS)
        self.assertEqual(response.json()['author'], self.user.id)
        self.assertEqual(response.json()['maker'], self.user.id)
        self.assertEqual(response.json()['description'][0]['text'], 'test_description')
        self.assertEqual(response.json()['comment'][0]['text'], 'test_comment')
        self.assertEqual(response.json()['project'], project_id)

        # Проверим фильтрацию
        response = self.client.get(reverse('task-list') + '?name=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(reverse('task-list') + '?name=bad_test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(reverse('task-list') + '?maker={}'.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(reverse('task-list') + '?maker={}'.format(self.user.id + 1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(reverse('task-list') + '?author={}'.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(reverse('task-list') + '?author={}'.format(self.user.id + 1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(reverse('task-list') + '?description=test_description')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(reverse('task-list') + '?name=bad_test_description')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(reverse('task-list') + '?project={}'.format(project_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(reverse('task-list') + '?project={}'.format(project_id + 1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        # Удалим задачу
        response = self.client.delete(reverse('task-detail', kwargs={'pk': task_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestTask(APITestCase):
    url = reverse('task-list')

    def setUp(self):
        self.user = User.objects.create(email='test@localhost.localdomain')
        self.user.set_password('abc1234')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(name='test task', status=Task.NEED, author=self.user)

    def test_get(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.all().count(), 1)

        response = self.client.get(self.url + '?name=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(self.url + '?name=test1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], Task.NEED)

    def test_post(self):
        data = {
            "name": "test1",
            "status": Task.NEED,
            "author": self.user.id,
            "maker": self.user.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        obj = Task.objects.filter(name=data['name'], status=data['status'], author=data['author'],
                                  maker=data['maker']).first()
        self.assertTrue(obj)

    def test_put(self):
        data = {
            "name": "test1-changed status",
            "status": Task.DONE,
            "author": self.user.id,
        }
        obj = Task.objects.all().first()

        response = self.client.put(reverse('task-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Task.objects.filter(id=obj.id).first()
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.status, data['status'])
        self.assertEqual(obj.author.id, data['author'])

    def test_patch(self):
        data = {
            "status": Task.DONE,
            "author": self.user.id
        }
        obj = Task.objects.all().first()

        response = self.client.patch(reverse('task-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Task.objects.filter(id=obj.id).first()
        self.assertEqual(obj.status, data['status'])


class TestDescription(APITestCase):
    url = reverse('description-list')

    def setUp(self):
        self.user = User.objects.create(email='test@localhost.localdomain')
        self.user.set_password('abc1234')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(name='test task', status=Task.NEED, author=self.user)

        self.description = Description.objects.create(text='test description')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Description.objects.all().count(), 1)

        response = self.client.get(reverse('description-detail', kwargs={'pk': self.description.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['text'], 'test description')

    def test_post(self):
        data = {
            "text": "test1",
            "task": self.task.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        obj = Description.objects.filter(text='test1', task=self.task).first()
        self.assertTrue(obj)

    def test_put(self):
        data = {
            "text": "test2",
            "task": self.task.id,
        }
        obj = Description.objects.create(text='test1')

        response = self.client.put(reverse('description-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Description.objects.get(id=obj.id)
        self.assertEqual(obj.text, data['text'])
        self.assertEqual(obj.task.id, data['task'])

    def test_patch(self):
        data = {
            "text": "test3"
        }
        obj = Description.objects.all().first()

        response = self.client.patch(reverse('description-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Description.objects.filter(id=obj.id).first()
        self.assertEqual(obj.text, data['text'])


class TestComment(APITestCase):
    url = reverse('comment-list')

    def setUp(self):
        self.user = User.objects.create(email='test@localhost.localdomain')
        self.user.set_password('abc1234')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(name='test task', status=Task.NEED, author=self.user)

        self.comment = Comment.objects.create(text='test comment')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.all().count(), 1)

        response = self.client.get(reverse('comment-detail', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['text'], 'test comment')

    def test_post(self):
        data = {
            "text": "test1",
            "task": self.task.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        obj = Comment.objects.filter(text='test1', task=self.task).first()
        self.assertTrue(obj)

    def test_put(self):
        data = {
            "text": "test2",
            "task": self.task.id,
        }
        obj = Comment.objects.create(text='test1')

        response = self.client.put(reverse('comment-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Comment.objects.get(id=obj.id)
        self.assertEqual(obj.text, data['text'])
        self.assertEqual(obj.task.id, data['task'])

    def test_patch(self):
        data = {
            "text": "test3"
        }
        obj = Comment.objects.all().first()

        response = self.client.patch(reverse('comment-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Comment.objects.filter(id=obj.id).first()
        self.assertEqual(obj.text, data['text'])


class TestProject(APITestCase):
    url = reverse('project-list')

    def setUp(self):
        self.user = User.objects.create(email='test@localhost.localdomain')
        self.user.set_password('abc1234')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(name='test project')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.all().count(), 1)

        response = self.client.get(reverse('project-detail', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test project')

    def test_post(self):
        data = {
            "name": "test1"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        obj = Project.objects.filter(name='test1').first()
        self.assertTrue(obj)

    def test_put_and_patch(self):
        data = {
            "name": "test2"
        }
        obj = Project.objects.create(name='test1')

        response = self.client.put(reverse('project-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Project.objects.get(id=obj.id)
        self.assertEqual(obj.name, data['name'])

    def test_patch(self):
        data = {
            "name": "test3"
        }
        obj = Project.objects.all().first()

        response = self.client.patch(reverse('project-detail', kwargs={'pk': obj.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Project.objects.filter(id=obj.id).first()
        self.assertEqual(obj.name, data['name'])
