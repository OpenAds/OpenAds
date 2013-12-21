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


class SuperuserViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'test@example.com', 'pass')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.provider = mommy.make(Provider)
        self.provider_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider)

        self.client.login(username='admin', password='pass')

    def test_can_view_provider_statistics(self):
        """
        Test that an admin can view any providers statistics page without issues
        """

        # Provider 1
        response = self.client.get(
            reverse('provider:stats', args=[self.provider.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], self.provider)

        # Second provider
        second_provider = mommy.make(Provider)

        response = self.client.get(
            reverse('provider:stats', args=[second_provider.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], second_provider)

        # A provider attached to the admin
        attached_provider = mommy.make(Provider, user=self.user)

        response = self.client.get(
            reverse('provider:stats', args=[attached_provider.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.context)
        self.assertEqual(response.context['provider'], attached_provider)

    def test_can_view_provider_list_page(self):
        """
        Test that an admin can view the admin overview page of all the providers
        """
        response = self.client.get(reverse('provider:list'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('providers', response.context)
        self.assertEqual(len(response.context["providers"]), 1)
        self.assertEqual(response.context["providers"][0], self.provider)

    def test_can_view_any_request_page(self):
        """
        Test that an admin can view their own request page
        """

        # Provider 1
        response = self.client.get(
            reverse('provider:request', args=[self.provider.pk])
        )

        self.assertEqual(response.status_code, 200)

        # Second provider
        second_provider = mommy.make(Provider)

        response = self.client.get(
            reverse('provider:request', args=[second_provider.pk])
        )

        self.assertEqual(response.status_code, 200)

        # A provider attached to the admin
        attached_provider = mommy.make(Provider, user=self.user)

        response = self.client.get(
            reverse('provider:request', args=[attached_provider.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_can_view_any_ad_statistics(self):
        """
        Test that an admin can view their own ad statistics
        """

        for advert in self.provider_adverts:
            response = self.client.get(reverse('provider:advert_statistics', args=[advert.pk]))

            self.assertEqual(response.status_code, 200)
            self.assertIn('advert', response.context)
            self.assertEqual(response.context['advert'], advert)

        # Provider attached to user
        attached_provider = mommy.make(Provider, user=self.user)
        attached_adverts = mommy.make(Advertisement, provider=attached_provider, _quantity=10)

        for advert in attached_adverts:
            response = self.client.get(reverse('provider:advert_statistics', args=[advert.pk]))

            self.assertEqual(response.status_code, 200)
            self.assertIn('advert', response.context)
            self.assertEqual(response.context['advert'], advert)


class UserViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'test@example.com', 'pass')
        self.user.save()

        self.provider = mommy.make(Provider)

        self.provider_adverts = mommy.make(Advertisement, _quantity=10, provider=self.provider)

        self.client.login(username='user', password='pass')

    def test_can_not_view_statistics(self):
        """
        Test that a normal user without a provider can not view a provider page
        """
        response = self.client.get(
            reverse('provider:stats', args=[self.provider.pk]),
            follow=True
        )

        self.assertEqual(response.status_code, 403)

    def test_can_not_view_provider_list_page(self):
        """
        Test that a normal user without a provider can not view the admin overview page of all the providers
        """
        response = self.client.get(reverse('provider:list'), follow=True)

        self.assertRedirects(response, reverse('accounts:login') + "?next=/list/")

    def test_can_not_view_request_page(self):
        """
        Test that a normal user without a provider can not view the request ad page
        """
        response = self.client.get(reverse('provider:request', args=[self.provider.pk]))

        self.assertEqual(response.status_code, 403)

    def test_can_not_view_ad_statistics(self):
        """
        Test that a normal user without a provider can not view ad statistics
        """

        for advert in self.provider_adverts:
            response = self.client.get(reverse('provider:advert_statistics', args=[advert.pk]))

            self.assertEqual(response.status_code, 403)


class AdvertisementViewTests(TestCase):
    def setUp(self):
        self.top_advert = mommy.make(Advertisement, ad_type=Advertisement.TOP_AD)
        self.side_adverts = mommy.make(Advertisement, ad_type=Advertisement.SIDE_AD, _quantity=4)

    def test_can_view_top(self):
        """
        Test that a user can view the top ad and that the top ad exists
        """
        response = self.client.get(reverse('advert:top'))

        self.assertEqual(response.status_code, 200)

        # Make sure that the ad properties are there
        self.assertContains(response, self.top_advert.image)

    def test_can_view_side_ads_without_login(self):
        """
        Test that a logged out user can view the side ads and that the side ads exist
        """
        response = self.client.get(reverse('advert:side'))

        self.assertEqual(response.status_code, 200)

        for advert in self.side_adverts:
            self.assertContains(response, advert.image)

    def test_only_active_ads_are_shown_on_top(self):
        """
        Test that only active adverts are shown on the top
        """

        # Inactive advert
        self.top_advert.status = Advertisement.INACTIVE
        self.top_advert.save()

        response = self.client.get(reverse('advert:top'))

        self.assertNotContains(response, self.top_advert.image)

        # Pending advert
        self.top_advert.status = Advertisement.PENDING
        self.top_advert.save()

        response = self.client.get(reverse('advert:top'))

        self.assertNotContains(response, self.top_advert.image)

    def test_only_active_ads_are_shown_on_side(self):
        """
        Test that only active adverts are shown on the side
        """

        # Inactive advert
        Advertisement.objects.filter(ad_type=Advertisement.SIDE_AD).update(status=Advertisement.INACTIVE)

        response = self.client.get(reverse('advert:side'))

        for advert in self.side_adverts:
            self.assertNotContains(response, advert.image)

        # Pending advert
        Advertisement.objects.filter(ad_type=Advertisement.SIDE_AD).update(status=Advertisement.PENDING)

        response = self.client.get(reverse('advert:side'))

        for advert in self.side_adverts:
            self.assertNotContains(response, advert.image)


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
