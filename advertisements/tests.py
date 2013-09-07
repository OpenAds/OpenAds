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

        self.provider_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider)
        self.provider2_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider2)

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
        response = self.client.get(
            reverse('advertisements.views.view_provider_statistics', args=[self.user.provider.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], self.provider)

    def test_can_not_view_other_statistics(self):
        """
        Test that a user can not view other peoples pages
        """
        response = self.client.get(reverse('advertisements.views.view_provider_statistics', args=[self.provider2.pk]))

        self.assertEqual(response.status_code, 404)

    def test_can_not_view_providers_page(self):
        """
        Test that a user can not view the admin overview page of all the providers
        """
        response = self.client.get(reverse('advertisements.views.providers_all'))

        self.assertEqual(response.status_code, 404)

    def test_can_view_own_ad_statistics(self):
        """
        Test that the user can view their own ad statistics
        """

        for advert in self.provider_adverts:
            response = self.client.get(reverse('advertisements.views.view_advert_statistics', args=[advert.pk]))

            self.assertEqual(response.status_code, 200)
            self.assertIn('advert', response.context)
            self.assertEqual(response.context['advert'], advert)

    def test_can_not_view_other_ad_statistics(self):
        """
        Test that the user can not view other ad statistics
        """

        for advert in self.provider2_adverts:
            response = self.client.get(reverse('advertisements.views.view_advert_statistics', args=[advert.pk]))

            self.assertEqual(response.status_code, 404)
