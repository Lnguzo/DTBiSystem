from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import InnovatorProfile, TalentPoolCohort, TalentPoolEvent, TalentPoolPhoto


class InnovatorPrivacyTests(TestCase):
    def make_user(self, username, user_type, *, is_staff=False):
        user = User.objects.create_user(username=username, password='test-password', is_staff=is_staff)
        user.profile.user_type = user_type
        user.profile.save(update_fields=['user_type'])
        return user

    def make_innovator(self, *, name, project, slug, phone, user=None):
        return InnovatorProfile.objects.create(
            innovator_name=name,
            project_name=project,
            slug=slug,
            catalogue='makisatu',
            description='A sample innovation profile.',
            phone_number=phone,
            user=user,
        )

    def test_public_directory_and_profile_never_render_phone_number(self):
        self.make_innovator(
            name='Public Innovator', project='Public Project', slug='public-project',
            phone='PRIVATE-PHONE-ALPHA',
        )

        directory = self.client.get(reverse('innovators'))
        profile = self.client.get(reverse('innovator_profile', args=['public-project']))

        self.assertEqual(directory.status_code, 200)
        self.assertEqual(profile.status_code, 200)
        self.assertNotContains(directory, 'PRIVATE-PHONE-ALPHA')
        self.assertNotContains(profile, 'PRIVATE-PHONE-ALPHA')
        self.assertNotContains(directory, 'Some entries only had a name')
        self.assertContains(directory, 'Explore Talent Pool')

    def test_innovator_directory_paginates_12_and_keeps_filters(self):
        for index in range(13):
            self.make_innovator(
                name=f'Test Innovator {index}',
                project=f'Test Project {index}',
                slug=f'test-project-{index}',
                phone='',
            )

        query = {'q': 'Test Innovator', 'catalogue': 'makisatu'}
        first_page = self.client.get(reverse('innovators'), query)
        second_page = self.client.get(reverse('innovators'), {**query, 'page': '2'})

        self.assertEqual(first_page.status_code, 200)
        self.assertEqual(first_page.context['page_obj'].paginator.count, 13)
        self.assertEqual(len(first_page.context['innovator_profiles']), 12)
        self.assertContains(first_page, 'Page 1 of 2')
        self.assertContains(first_page, 'catalogue=makisatu&amp;page=2')
        self.assertEqual(len(second_page.context['innovator_profiles']), 1)
        self.assertEqual(second_page.context['page_obj'].number, 2)

    def test_innovator_dashboard_only_shows_records_linked_to_that_account(self):
        innovator_user = self.make_user('innovator-one', 'innovator')
        another_user = self.make_user('innovator-two', 'innovator')
        self.make_innovator(
            name='Innovator One', project='One Project', slug='one-project',
            phone='PRIVATE-PHONE-ONE', user=innovator_user,
        )
        self.make_innovator(
            name='Innovator Two', project='Two Project', slug='two-project',
            phone='PRIVATE-PHONE-TWO', user=another_user,
        )

        login_response = self.client.post(reverse('staff:user_login'), {
            'username': 'innovator-one',
            'password': 'test-password',
        })
        self.assertRedirects(login_response, reverse('staff:account_dashboard'))
        response = self.client.get(reverse('staff:account_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile'].user_type, 'innovator')
        self.assertContains(response, 'PRIVATE-PHONE-ONE')
        self.assertNotContains(response, 'PRIVATE-PHONE-TWO')

    def test_only_staff_or_admin_can_open_all_innovator_records(self):
        innovator_user = self.make_user('innovator-user', 'innovator')
        staff_user = self.make_user('staff-user', 'staff', is_staff=True)
        self.make_innovator(
            name='A Private Innovator', project='Private Project', slug='private-project',
            phone='PRIVATE-PHONE-STAFF-ONLY',
        )

        response = self.client.get(reverse('staff:innovator_management'))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(innovator_user)
        response = self.client.get(reverse('staff:innovator_management'))
        self.assertEqual(response.status_code, 403)

        self.client.force_login(staff_user)
        response = self.client.get(reverse('staff:innovator_management'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PRIVATE-PHONE-STAFF-ONLY')
        self.assertContains(response, reverse('staff:innovator_management'))


class TalentPoolPageTests(TestCase):
    def test_participant_session_photo_is_shown_on_talent_pool_page(self):
        response = self.client.get(reverse('talent_pool'), {'cohort': 'talent-pool-2026'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Talent Pool participants during a learning session')
        self.assertContains(response, 'talent-pool-2026-participants-session.jpg')
        self.assertNotContains(response, 'Programme at a glance')
        self.assertContains(response, 'Meet the innovators')

    def test_published_cohort_event_and_gallery_render(self):
        cohort = TalentPoolCohort.objects.create(
            title='Sample Talent Pool',
            slug='sample-talent-pool',
            year=2026,
            summary='A sample cohort.',
            description='A sample programme description.',
            status='completed',
            is_featured=True,
            is_published=True,
        )
        event = TalentPoolEvent.objects.create(
            cohort=cohort,
            title='Sample Demo Day',
            description='Participants presented their work.',
            is_published=True,
        )
        TalentPoolPhoto.objects.create(
            event=event,
            image_path='img/talent-pool/sample.jpg',
            caption='Sample event photo',
            alt_text='Participants at a demo day',
        )

        response = self.client.get(reverse('talent_pool'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Talent Pool')
        self.assertContains(response, 'Sample Demo Day')
        self.assertContains(response, 'Sample event photo')
        self.assertContains(response, 'Meet the innovators')
