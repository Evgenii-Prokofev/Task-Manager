from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from task_manager.statuses.models import Status
from task_manager.fixtures.parser_json_data import parse_json_data


# Create your tests here.
class StatusesCRUDTestCase(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        statuses_data = parse_json_data(settings.DUMP_DATA_PATH, "statuses")
        self.new_status = statuses_data["new_status"]
        self.update_status = statuses_data["update_status"]

    def test_create_status(self):
        response = self.client.get(reverse('statuses_create'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('statuses_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

        response = self.client.post(
            reverse('statuses_create'),
            data=self.new_status,
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertContains(response, _('Status successfully created'))

        last_status = Status.objects.last()
        count_statuses = Status.objects.count()
        self.assertEqual(last_status.name, "new")
        self.assertEqual(str(last_status), "new")
        self.assertEqual(count_statuses, 3)

    def test_read_statuses(self):
        response = self.client.get(reverse('statuses'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertEqual(len(response.context['statuses']), 2)
        self.assertContains(response, "in progress")
        self.assertContains(response, "finished")

    def test_update_status(self):
        response = self.client.get(
            reverse('statuses_update', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(
            reverse('statuses_update', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

        response = self.client.post(
            reverse('statuses_update', kwargs={"pk": 1}),
            data=self.update_status,
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertContains(response, _('Status successfully changed'))
        self.assertEqual(Status.objects.get(pk=1).name, "on testing")

    def test_delete_status(self):
        response = self.client.get(
            reverse('statuses_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))

        response = self.client.get(
            reverse('statuses_delete', kwargs={"pk": 2}), follow=True
        )
        self.assertTemplateUsed(response, 'statuses/delete.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "finished")

        response = self.client.post(
            reverse('statuses_delete', kwargs={"pk": 2}), follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 1)
        self.assertContains(response, _('Status successfully deleted'))
