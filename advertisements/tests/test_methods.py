from django.test import TestCase
from advertisements.models import User, Provider, Advertisement
from model_mommy import mommy


class ProviderCountMethodTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'test@example.com', 'pass')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.provider = Provider(
            name='provider',
            user=self.user,
        )
        self.provider.save()

        self.provider_active_adverts = mommy.make(
            Advertisement, _quantity=20,
            provider=self.provider,
            status=Advertisement.ACTIVE
        )
        self.provider_inactive_adverts = mommy.make(
            Advertisement, _quantity=20,
            provider=self.provider,
            status=Advertisement.INACTIVE
        )
        self.provider_pending_adverts = mommy.make(
            Advertisement, _quantity=20,
            provider=self.provider,
            status=Advertisement.PENDING
        )

    def tearDown(self):
        self.provider.delete()
        self.user.delete()

    def test_active_ads_returns_correct_amounts(self):
        """
        Test that the active_ads method on a provider returns the correct amount
        """
        self.assertEqual(self.provider.active_ads(), 20)

    def test_inactive_ads_returns_correct_amounts(self):
        """
        Test that the inactive_ads method on a provider returns the correct amount
        """
        self.assertEqual(self.provider.inactive_ads(), 20)