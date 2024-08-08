from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from task_manager.fixtures.parser_json_data import parse_json_data
from task_manager.labels.models import Label


# Create your tests here.
class LabelCRUDTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        labels_data = parse_json_data(settings.DUMP_DATA_PATH, "labels")
        self.new_label = labels_data["new_label"]
        self.update_label = labels_data["update_label"]

    def test_create_label(self):
        response = self.client.get(reverse('labels_create'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('labels_create'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

        response = self.client.post(
            reverse('labels_create'),
            data=self.new_label,
            follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertContains(response, _("Label successfully created"))

        last_label = Label.objects.last()
        count_labels = Label.objects.count()
        self.assertEqual(last_label.name, "New label")
        self.assertEqual(str(last_label), "New label")
        self.assertEqual(count_labels, 4)

    def test_read_labels(self):
        response = self.client.get(reverse('labels'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('labels'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')
        self.assertEqual(len(response.context['labels']), 3)
        self.assertContains(response, "mine")
        self.assertContains(response, "not mine")
        self.assertContains(response, "warning")

    def test_update_label(self):
        response = self.client.get(
            reverse('labels_update', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=2))
        response = self.client.get(
            reverse('labels_update', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

        response = self.client.post(
            reverse('labels_update', kwargs={"pk": 1}),
            data=self.update_label,
            follow=True
        )
        new_label = Label.objects.get(pk=1)
        self.assertRedirects(response, reverse('labels'))
        self.assertContains(response, _("Label successfully changed"))
        self.assertEqual(new_label.name, "Red label")

    def test_delete_label(self):
        self.client.force_login(get_user_model().objects.get(pk=2))
        response = self.client.get(
            reverse('labels_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "mine")

        response = self.client.post(
            reverse('labels_delete', kwargs={"pk": 3}), follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 2)
        self.assertContains(response, _("Label successfully deleted"))
