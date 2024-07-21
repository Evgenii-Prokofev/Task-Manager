from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.fixtures.parser_json_data import parse_json_data
from django.conf import settings


# Create your tests here.
class UserCRUDTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        users_data = parse_json_data(settings.DUMP_DATA_PATH, "users")
        self.new_user = users_data["new_user"]
        self.wrong_update_user = users_data["wrong_update_user"]
        self.success_update_user = users_data["success_update_user"]

    def test_create_user(self):
        response = self.client.get(reverse('user_create'))
        self.assertTemplateUsed(response, 'users/create.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_create'),
            data=self.new_user,
            follow=True,
        )
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('User is successfully registered'))

        last_user = User.objects.last()
        users_count = User.objects.count()
        self.assertEqual(last_user.first_name, "Ivan")
        self.assertEqual(last_user.last_name, "Ivanov")
        self.assertEqual(last_user.username, "Vanya")
        self.assertEqual(str(last_user), "Ivan Ivanov")
        self.assertEqual(users_count, 4)

    def test_read_users(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertContains(response, 'Georgiy Zhukov')
        self.assertContains(response, 'Konstantin Rokossovskiy')
        self.assertContains(response, 'Vasiliy Chuikov')
        self.assertEqual(len(response.context['users']), 3)

    def test_update_user(self):
        response = self.client.get(
            reverse('user_update', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))

        response = self.client.get(
            reverse('user_update', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response, _("You don't have permissions to modify another user.")
        )

        response = self.client.get(
            reverse('user_update', kwargs={'pk': 1}),
            follow=True
        )
        self.assertTemplateUsed(response, 'users/update.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_update', kwargs={'pk': 1}),
            data=self.wrong_update_user,
            follow=True
        )
        response_content = response.content.decode()
        assert "Введенные пароли не совпадают." in response_content

        response = self.client.post(
            reverse('user_update', kwargs={'pk': 1}),
            data=self.success_update_user,
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('User is successfully updated'))
        self.assertEqual(User.objects.get(pk=1).username, "Footbolist")

    def test_delete_user(self):
        response = self.client.get(
            reverse('user_delete', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=3))

        response = self.client.get(
            reverse('user_delete', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response, _("You don't have permissions to modify another user.")
        )

        response = self.client.get(
            reverse('user_delete', kwargs={'pk': 3}),
            follow=True
        )
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vasiliy Chuikov')

        response = self.client.post(
            reverse('user_delete', kwargs={'pk': 3}),
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertContains(response, _('User is successfully deleted'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)
