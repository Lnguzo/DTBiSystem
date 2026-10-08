from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import DataImportBatch, Investor, Mentor, Startup, UserProfile


class ImportDestinationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username='importdestinationadmin',
            email='importdestination@example.com',
            password='secret1234',
        )
        UserProfile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def _upload_preview_and_confirm(self, dataset, csv_text, filename):
        initial_count = self._record_count(dataset)
        response = self.client.post(reverse('staff:data_import'), {
            'action': 'upload',
            'dataset': dataset,
            'file': SimpleUploadedFile(filename, csv_text.encode(), content_type='text/csv'),
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '>Preview</button>')
        self.assertContains(response, '>Upload records</button>')
        batch = response.context['batch']
        self.assertEqual(batch.status, 'preview')
        self.assertEqual(self._record_count(dataset), initial_count)

        check_data = {'action': 'check', 'batch_id': batch.pk}
        check_data.update({
            f'map_{field}': header
            for field, header in batch.field_mapping.items()
        })
        response = self.client.post(reverse('staff:data_import'), check_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '>Upload records</button>')
        self.assertEqual(response.context['preview_analysis']['creates'], 1)
        self.assertEqual(self._record_count(dataset), initial_count)

        response = self.client.post(reverse('staff:data_import'), {
            **check_data,
            'action': 'confirm',
        })
        self.assertRedirects(response, f"{reverse('staff:data_import')}?batch={batch.pk}")
        batch.refresh_from_db()
        self.assertEqual(batch.status, 'completed')
        self.assertEqual(batch.created_count, 1)
        self.assertEqual(self._record_count(dataset), initial_count + 1)

        response = self.client.get(reverse('staff:data_import'), {'batch': batch.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{self._destination(dataset)}"')
        return batch

    @staticmethod
    def _record_count(dataset):
        models = {
            'startup': Startup,
            'mentor': Mentor,
            'investor': Investor,
        }
        return models[dataset].objects.count()

    @staticmethod
    def _destination(dataset):
        route_names = {
            'startup': 'staff:startups',
            'mentor': 'mentors',
            'investor': 'investors',
        }
        return reverse(route_names[dataset])

    def test_startup_import_is_added_to_public_startup_directory(self):
        self._upload_preview_and_confirm(
            'startup',
            'Startup Name,Industry,Website,Contact Email\n'
            'Imported Startup,Agriculture,https://imported.example,hello@imported.example\n',
            'startups.csv',
        )
        startup = Startup.objects.get(name='Imported Startup')
        self.assertEqual(startup.status, 'active')

        self.client.logout()
        response = self.client.get(reverse('staff:startups'))
        self.assertContains(response, 'Imported Startup')

    def test_mentor_import_is_added_to_mentor_directory(self):
        self._upload_preview_and_confirm(
            'mentor',
            'Name,Email,Role,Skills\n'
            'Imported Mentor,mentor@imported.example,Advisor,Finance\n',
            'mentors.csv',
        )
        self.assertTrue(Mentor.objects.get(name='Imported Mentor').is_active)

        self.client.logout()
        response = self.client.get(reverse('mentors'))
        self.assertContains(response, 'Imported Mentor')

    def test_investor_import_is_added_to_investor_directory(self):
        self._upload_preview_and_confirm(
            'investor',
            'Name,Organization,Email,Investment Interest\n'
            'Imported Investor,Example Capital,investor@imported.example,Climate technology\n',
            'investors.csv',
        )
        self.assertEqual(Investor.objects.get(name='Imported Investor').status, 'active')

        self.client.logout()
        response = self.client.get(reverse('investors'))
        self.assertContains(response, 'Imported Investor')
