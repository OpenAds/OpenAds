from django.test import TestCase
from django.contrib.auth.models import User
from advertisements.models import User, Provider, Advertisement
from django.core.urlresolvers import reverse
from model_mommy import mommy


class ProviderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('provider', 'test@example.com', 'pass')
        self.provider = Provider(
            name='provider',
            user=self.user,
        )
        self.provider.save()

        self.provider2 = Provider(
            name='provider2'
        )
        self.provider2.save()

        self.client.login(username='provider', password='pass')

    def tearDown(self):
        self.client.logout()
        self.provider.delete()
        self.provider2.delete()
        self.user.delete()

    def test_can_view_own_statistics(self):
        """
        Test that a user can view their own provider page without problems
        """
        response = self.client.get(reverse('advertisements.views.view_provider_statistics', args=[self.user.provider.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], self.provider)

    def test_can_not_view_other_statistics(self):
        """
        Test that a user can not view other peoples pages
        """
        response = self.client.get(reverse('advertisements.views.view_provider_statistics', args=[self.provider2.pk]))

        self.assertEqual(response.status_code, 404)

