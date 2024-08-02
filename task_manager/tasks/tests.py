from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from task_manager.fixtures.parser_json_data import parse_json_data
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


# Create your tests here.
class TaskCRUDTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json']

    def setUp(self):
        tasks_data = parse_json_data(settings.DUMP_DATA_PATH, "tasks")
        self.new_task = tasks_data["new_task"]
        self.new_task["status"] = Status.objects.get(pk=1).pk
        self.update_task = tasks_data["update_task"]
        self.update_task["status"] = Status.objects.get(pk=2).pk

    def test_create_task(self):
        response = self.client.get(reverse('tasks_create'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

        response = self.client.post(
            reverse('tasks_create'),
            data=self.new_task,
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        last_task = Task.objects.last()
        count_tasks = Task.objects.count()
        self.assertEqual(last_task.name, "Task 2")
        self.assertEqual(str(last_task), "Task 2")
        self.assertEqual(last_task.status.name, "in progress")
        self.assertEqual(count_tasks, 2)

    def test_read_tasks_list(self):
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertEqual(len(response.context['tasks']), 2)
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")

    def test_read_task_detail(self):
        response = self.client.get(
            reverse('task_show', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(
            reverse('task_show', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/show.html')
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Georgiy Zhukov")
        self.assertContains(response, "Konstantin Rokossovskiy")
        self.assertContains(response, "in progress")

    def test_update_task(self):
        response = self.client.get(
            reverse('tasks_update', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(
            reverse('tasks_update', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

        response = self.client.post(
            reverse('tasks_update', kwargs={"pk": 1}),
            data=self.update_task,
            follow=True
        )
        new_task = Task.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_task.name, "Task 1")
        self.assertEqual(new_task.status.name, "in progress")

    def test_delete_task(self):
        response = self.client.get(
            reverse('tasks_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=2))

        response = self.client.get(
            reverse('tasks_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")

        response = self.client.post(
            reverse('tasks_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertContains(
            response, _("The task can be deleted only by its author")
        )
        self.assertEqual(Task.objects.count(), 2)

        response = self.client.post(
            reverse('tasks_delete', kwargs={"pk": 2}), follow=True
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 1)
        self.assertContains(response, _('Task successfully deleted'))
