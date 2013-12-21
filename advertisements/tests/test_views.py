from django.test import TestCase
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

        self.provider_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider)

        self.client.login(username='provider', password='pass')

    def test_home_redirects_to_own_statistics(self):
        """
        Test that a provider is redirected to their provider statistics page when visiting the home page
        """
        response = self.client.get(reverse('provider:home'), follow=True)

        # Make sure it redirected
        self.assertRedirects(response, reverse('provider:stats', args=[self.provider.pk]))

        # Make sure it ended up at the right place
        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], self.provider)

    def test_can_view_own_statistics(self):
        """
        Test that a provider can view their own provider page without problems
        """
        response = self.client.get(
            reverse('provider:stats', args=[self.provider.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], self.provider)

    def test_visiting_other_provider_page_returns_own_provider(self):
        """
        Test that when a provider visits another provider's statistics page, they still get their own
        """
        other_provider = mommy.make(Provider)

        response = self.client.get(
            reverse('provider:stats', args=[other_provider.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], self.provider)

    def test_can_view_own_request_page(self):
        """
        Test that a provider can view their own request page without problems
        """
        response = self.client.get(
            reverse('provider:request', args=[self.provider.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_can_not_view_provider_list_page(self):
        """
        Test that a provider can not view the admin overview page of all the providers. They should be redirected
        to a login page
        """
        response = self.client.get(reverse('provider:list'), follow=True)

        self.assertRedirects(response, reverse('accounts:login') + "?next=/list/")

    def test_can_view_own_ad_statistics(self):
        """
        Test that a provider can view their own ad statistics
        """

        for advert in self.provider_adverts:
            response = self.client.get(reverse('provider:advert_statistics', args=[advert.pk]))

            self.assertEqual(response.status_code, 200)
            self.assertIn('advert', response.context)
            self.assertEqual(response.context['advert'], advert)

    def test_can_not_view_other_ad_statistics(self):
        """
        Test that a provider can not view other ad statistics
        """

        other_provider_adverts = mommy.make(Advertisement, _quantity=5)

        for advert in other_provider_adverts:
            response = self.client.get(reverse('provider:advert_statistics', args=[advert.pk]))

            self.assertEqual(response.status_code, 404)


#class SuperuserViewTests(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user('admin', 'test@example.com', 'pass')
#        self.user.is_superuser = True
#        self.user.is_staff = True
#        self.user.save()
#
#        self.provider = Provider(
#            name='provider',
#            user=self.user,
#        )
#        self.provider.save()
#
#        self.provider2 = Provider(
#            name='provider2'
#        )
#        self.provider2.save()
#
#        self.provider_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider)
#        self.provider2_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider2)
#
#        self.client.login(username='admin', password='pass')
#
#    def tearDown(self):
#        self.client.logout()
#        self.provider.delete()
#        self.provider2.delete()
#        self.user.delete()
#
#    def test_can_view_own_statistics(self):
#        """
#        Test that an admin can view their own provider page without problems
#        """
#        response = self.client.get(
#            reverse('advertisements.views.view_provider_statistics', args=[self.user.provider.pk])
#        )
#
#        self.assertEqual(response.status_code, 200)
#        self.assertIn('provider', response.context)
#        self.assertEqual(response.context['provider'], self.provider)
#
#    def test_can_view_other_statistics(self):
#        """
#        Test that an admin can view other peoples pages
#        """
#        response = self.client.get(reverse('advertisements.views.view_provider_statistics', args=[self.provider2.pk]))
#
#        self.assertEqual(response.status_code, 200)
#        self.assertIn('provider', response.context)
#        self.assertEqual(response.context['provider'], self.provider2)
#
#    def test_can_view_providers_page(self):
#        """
#        Test that an admin can view the admin overview page of all the providers
#        """
#        response = self.client.get(reverse('advertisements.views.providers_all'))
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_view_own_request_page(self):
#        """
#        Test that an admin can view their own request page
#        """
#        response = self.client.get(reverse('advertisements.views.provider_request', args=[self.provider.pk]))
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_view_other_request_pages(self):
#        """
#        Test that an admin can view other request pages
#        """
#        response = self.client.get(reverse('advertisements.views.provider_request', args=[self.provider2.pk]))
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_view_own_ad_statistics(self):
#        """
#        Test that an admin can view their own ad statistics
#        """
#
#        for advert in self.provider_adverts:
#            response = self.client.get(reverse('advertisements.views.view_advert_statistics', args=[advert.pk]))
#
#            self.assertEqual(response.status_code, 200)
#            self.assertIn('advert', response.context)
#            self.assertEqual(response.context['advert'], advert)
#
#    def test_can_view_other_ad_statistics(self):
#        """
#        Test that an admin can view other ad statistics
#        """
#
#        for advert in self.provider2_adverts:
#            response = self.client.get(reverse('advertisements.views.view_advert_statistics', args=[advert.pk]))
#
#            self.assertEqual(response.status_code, 200)
#            self.assertIn('advert', response.context)
#            self.assertEqual(response.context['advert'], advert)
#
#
#class UserViewTests(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user('user', 'test@example.com', 'pass')
#        self.user.save()
#
#        self.provider = Provider(
#            name='provider',
#        )
#        self.provider.save()
#
#        self.provider_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider)
#
#        self.client.login(username='user', password='pass')
#
#    def tearDown(self):
#        self.client.logout()
#        self.provider.delete()
#        self.user.delete()
#
#    def test_can_not_view_statistics(self):
#        """
#        Test that a normal user without a provider can not view a provider page
#        """
#        response = self.client.get(
#            reverse('advertisements.views.view_provider_statistics', args=[self.provider.pk]),
#            follow=True
#        )
#
#        self.assertEqual(len(response.redirect_chain), 2)
#
#        self.assertEqual(response.redirect_chain[0][0], 'http://testserver' + reverse('accounts:logout'))
#        self.assertEqual(response.redirect_chain[0][1], 302)
#
#        self.assertEqual(response.redirect_chain[1][0], 'http://testserver' + reverse('accounts:login'))
#        self.assertEqual(response.redirect_chain[1][1], 302)
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_not_view_providers_page(self):
#        """
#        Test that a normal user without a provider can not view the admin overview page of all the providers
#        """
#        response = self.client.get(reverse('advertisements.views.providers_all'), follow=True)
#
#        self.assertEqual(len(response.redirect_chain), 2)
#
#        self.assertEqual(response.redirect_chain[0][0], 'http://testserver' + reverse('accounts:logout'))
#        self.assertEqual(response.redirect_chain[0][1], 302)
#
#        self.assertEqual(response.redirect_chain[1][0], 'http://testserver' + reverse('accounts:login'))
#        self.assertEqual(response.redirect_chain[1][1], 302)
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_not_view_request_page(self):
#        """
#        Test that a normal user without a provider can not view the request ad page
#        """
#        response = self.client.get(
#            reverse('advertisements.views.provider_request', args=[self.provider.pk]),
#            follow=True
#        )
#
#        self.assertEqual(len(response.redirect_chain), 2)
#
#        self.assertEqual(response.redirect_chain[0][0], 'http://testserver' + reverse('accounts:logout'))
#        self.assertEqual(response.redirect_chain[0][1], 302)
#
#        self.assertEqual(response.redirect_chain[1][0], 'http://testserver' + reverse('accounts:login'))
#        self.assertEqual(response.redirect_chain[1][1], 302)
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_not_view_ad_statistics(self):
#        """
#        Test that a normal user without a provider can not view ad statistics
#        """
#
#        for advert in self.provider_adverts:
#            response = self.client.get(
#                reverse('advertisements.views.view_advert_statistics', args=[advert.pk]),
#                follow=True
#            )
#
#            self.assertEqual(len(response.redirect_chain), 2)
#
#            self.assertEqual(response.redirect_chain[0][0], 'http://testserver' + reverse('accounts:logout'))
#            self.assertEqual(response.redirect_chain[0][1], 302)
#
#            self.assertEqual(response.redirect_chain[1][0], 'http://testserver' + reverse('accounts:login'))
#            self.assertEqual(response.redirect_chain[1][1], 302)
#
#            self.assertEqual(response.status_code, 200)
#
#
#class AdvertisementViewTests(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user('admin', 'test@example.com', 'pass')
#        self.user.is_superuser = True
#        self.user.is_staff = True
#        self.user.save()
#
#        self.provider = Provider(
#            name='provider',
#            user=self.user,
#        )
#        self.provider.save()
#
#        self.provider_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider)
#
#        self.client.login(username='admin', password='pass')
#
#    def tearDown(self):
#        self.client.logout()
#        self.provider.delete()
#        self.user.delete()
#
#    def test_can_view_top_ads_with_login(self):
#        """
#        Test that a logged in user can view the top ads
#        """
#        response = self.client.get(reverse('advertisements.views.top_ad'))
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_view_side_ads_with_login(self):
#        """
#        Test that a logged in user can view the side ads
#        """
#        response = self.client.get(reverse('advertisements.views.side_ads'))
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_view_top_ads_without_login(self):
#        """
#        Test that a logged out user can view the top ads
#        """
#        self.client.logout()
#        response = self.client.get(reverse('advertisements.views.top_ad'))
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_can_view_side_ads_without_login(self):
#        """
#        Test that a logged out user can view the side ads
#        """
#        self.client.logout()
#        response = self.client.get(reverse('advertisements.views.side_ads'))
#
#        self.assertEqual(response.status_code, 200)
#
#
#class ClickRegisterTest(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user('admin', 'test@example.com', 'pass')
#        self.user.is_superuser = True
#        self.user.is_staff = True
#        self.user.save()
#
#        self.provider = Provider(
#            name='provider',
#            user=self.user,
#        )
#        self.provider.save()
#
#        self.provider_adverts = mommy.make(Advertisement, _quantity=200, provider=self.provider)
#
#    def tearDown(self):
#        self.provider.delete()
#        self.user.delete()
#
#    def test_user_click_goes_to_url(self):
#        """
#        Test that the click redirects the user to the site url
#        """
#        for advert in self.provider_adverts:
#            response = self.client.get(advert.get_signed_link(), follow=True)
#
#            self.assertEqual(response.redirect_chain[0][0], advert.url)
#            self.assertEqual(response.redirect_chain[0][1], 302)
#
#    def test_click_increments_advertisement_clicks(self):
#        """
#        Test that the click on an ad increments the click total
#        """
#        for advert in self.provider_adverts:
#            self.assertEqual(advert.click_set.count(), 0)
#
#            for i in range(20):
#                response = self.client.get(
#                    advert.get_signed_link(),
#                    follow=True
#                )
#                self.assertEqual(advert.click_set.count(), i+1)
