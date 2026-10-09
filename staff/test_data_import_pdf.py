from io import BytesIO
from unittest.mock import Mock, patch
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .data_services import (
    _ocr_pdf_page, _pdf_attribute_rows, _pdf_page_rows, guess_field_mapping, read_import_file,
)
from .models import Startup, UserProfile


class PdfDataImportTests(SimpleTestCase):
    def test_prefers_record_type_attribute_table_over_multicolumn_page_text(self):
        table = [
            ['Founder and Startup Name', 'Employment Created', 'Product (Service Offered)'],
            ['Amina Kato - Nuru Foods', '3 Employees', 'Fruit snacks'],
            ['Years of Operation', 'Investment Raised', 'Website and Links'],
            ['4 Years', '25,000 USD', 'https://nuru.example/ profile'],
        ]
        noisy_page_text = [
            ['Company narrative broken into many columns'],
            ['paragraph', 'fragments', 'from', 'the', 'page'],
            ['more', 'unrelated', 'narrative', 'fragments', 'here'],
        ]
        page = Mock()
        page.extract_tables.side_effect = [[table], [noisy_page_text]]

        expected_table = [row[:] for row in table]
        expected_table[3][2] = 'https://nuru.example/ profile'
        self.assertEqual(_pdf_page_rows(page, dataset='startup'), expected_table)

    def test_converts_record_type_attribute_table_to_platform_startup_fields(self):
        rows = [
            ['Founder and Startup Name', 'Employment Created', 'Product (Service Offered)'],
            ['Amina Kato - Nuru Foods', '3 Employees', 'Fruit snacks'],
            ['Years of Operation', 'Investment Raised', 'Website and Links'],
            ['4 Years', '25,000 USD', 'https://nuru.example/ profile'],
            ['Business Description', 'Link to Buni Hub (DTBi)', ''],
            ['Produces fruit snacks locally', 'Joined BUNI programme', ''],
        ]

        imported = _pdf_attribute_rows(rows, 'startup')

        headers, values = imported
        mapping = guess_field_mapping('startup', headers)
        record = {field: values[headers.index(header)] for field, header in mapping.items()}
        self.assertEqual(record['name'], 'Nuru Foods')
        self.assertEqual(record['contact_person'], 'Amina Kato')
        self.assertEqual(record['website'], 'https://nuru.example/profile')
        self.assertIn('3 Employees', record['description'])
        self.assertIn('Fruit snacks', record['description'])
        self.assertIn('4 Years', record['description'])
        self.assertIn('25,000 USD', record['description'])
        self.assertIn('Produces fruit snacks locally', record['description'])

    def test_reads_borderless_pdf_columns_and_skips_repeated_page_headers(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'startups.pdf'
            document = canvas.Canvas(str(path), pagesize=letter)
            columns = (40, 220, 370)
            pages = [
                [
                    ('Startup Name', 'Industry', 'Contact Email'),
                    ('Agri Green Ltd', 'Agriculture', 'hello@agri.example'),
                ],
                [
                    ('Startup Name', 'Industry', 'Contact Email'),
                    ('Finance Rise', 'Finance', 'contact@finance.example'),
                ],
            ]
            for page_rows in pages:
                y = 750
                for row in page_rows:
                    for x, value in zip(columns, row):
                        document.drawString(x, y, value)
                    y -= 20
                document.showPage()
            document.save()

            headers, records = read_import_file(path)

        self.assertEqual(headers, ['Startup Name', 'Industry', 'Contact Email'])
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['Startup Name'], 'Agri Green Ltd')
        self.assertEqual(records[1]['Contact Email'], 'contact@finance.example')
        mapping = guess_field_mapping('startup', headers)
        self.assertEqual(mapping['name'], 'Startup Name')
        self.assertEqual(mapping['industry'], 'Industry')
        self.assertEqual(mapping['contact_email'], 'Contact Email')

    def test_rejects_non_table_pdf_with_actionable_error(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'no-table.pdf'
            document = canvas.Canvas(str(path), pagesize=letter)
            document.drawString(40, 750, 'This PDF has no tabular data.')
            document.save()

            with self.assertRaisesMessage(ValidationError, 'No readable text or table was found'):
                read_import_file(path)

    def test_reads_labeled_pdf_records_using_selected_startup_fields(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'startup-profiles.pdf'
            document = canvas.Canvas(str(path), pagesize=letter)
            document.drawString(40, 750, 'Startup Name: Agri Green Ltd')
            document.drawString(40, 730, 'Industry: Agriculture')
            document.drawString(40, 710, 'Contact Email: hello@agri.example')
            document.drawString(40, 680, 'Startup Name: Finance Rise')
            document.drawString(40, 660, 'Industry: Financial Technology')
            document.drawString(40, 640, 'Contact Email: contact@finance.example')
            document.save()

            headers, records = read_import_file(path, dataset='startup')

        self.assertEqual(len(records), 2)
        mapping = guess_field_mapping('startup', headers)
        self.assertEqual(records[0][mapping['name']], 'Agri Green Ltd')
        self.assertEqual(records[0][mapping['industry']], 'Agriculture')
        self.assertEqual(records[1][mapping['contact_email']], 'contact@finance.example')

    @patch(
        'staff.data_services._ocr_pdf_page',
        return_value=(
            'Startup Name: TechNova Tanzania\nIndustry: FinTech\nContact Emall hello@technova.example',
            [],
        ),
    )
    def test_ocr_text_is_sorted_into_selected_startup_fields(self, _mock_ocr):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'scanned-startup.pdf'
            document = canvas.Canvas(str(path), pagesize=letter)
            document.showPage()
            document.save()

            headers, records = read_import_file(path, dataset='startup')

        mapping = guess_field_mapping('startup', headers)
        self.assertEqual(records[0][mapping['name']], 'TechNova Tanzania')
        self.assertEqual(records[0][mapping['industry']], 'FinTech')
        self.assertEqual(records[0][mapping['contact_email']], 'hello@technova.example')
        _mock_ocr.assert_called_once()

    @patch(
        'staff.data_services._ocr_pdf_page',
        return_value=(
            'Startup Name Industry Contact Email\nTechNova Tanzania FinTech hello@technova.example',
            [
                ['Startup Name', 'Industry', 'Contact Email'],
                ['TechNova Tanzania', 'FinTech', 'hello@technova.example'],
            ],
        ),
    )
    def test_ocr_table_columns_are_mapped_to_the_selected_record_type(self, _mock_ocr):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'scanned-startup-table.pdf'
            document = canvas.Canvas(str(path), pagesize=letter)
            document.showPage()
            document.save()

            headers, records = read_import_file(path, dataset='startup')

        mapping = guess_field_mapping('startup', headers)
        self.assertEqual(records[0][mapping['name']], 'TechNova Tanzania')
        self.assertEqual(records[0][mapping['industry']], 'FinTech')
        self.assertEqual(records[0][mapping['contact_email']], 'hello@technova.example')
        _mock_ocr.assert_called_once()

    @patch('pytesseract.image_to_data')
    def test_ocr_aligns_scanned_table_values_using_header_columns(self, mock_image_to_data):
        tokens = [
            (100, 100, 130, 'Startup'), (250, 100, 110, 'Name'),
            (600, 100, 150, 'Industry'), (1050, 100, 130, 'Contact'),
            (1200, 100, 100, 'Email'),
            (100, 200, 220, 'TechNova'), (340, 200, 140, 'Tanzania'),
            (600, 200, 150, 'FinTech'), (1050, 200, 250, 'hello@technova.example'),
        ]
        mock_image_to_data.return_value = {
            'text': [token[3] for token in tokens],
            'left': [token[0] for token in tokens],
            'top': [token[1] for token in tokens],
            'height': [40 for _token in tokens],
            'width': [token[2] for token in tokens],
            'block_num': [1 for _token in tokens],
            'par_num': [1 for _token in tokens],
            'line_num': [1 if token[1] == 100 else 2 for token in tokens],
        }
        page = Mock()
        page.to_image.return_value.original = Mock()

        text, rows = _ocr_pdf_page(page, dataset='startup')

        self.assertIn('TechNova Tanzania FinTech', text)
        self.assertEqual(rows, [
            ['Startup Name', 'Industry', 'Contact Email'],
            ['TechNova Tanzania', 'FinTech', 'hello@technova.example'],
        ])


class PdfImportFieldFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username='pdfimportadmin',
            email='pdfimportadmin@example.com',
            password='secret1234',
        )
        UserProfile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def test_extracted_pdf_values_prefill_fields_and_import_from_them(self):
        pdf_content = BytesIO()
        document = canvas.Canvas(pdf_content, pagesize=letter)
        document.drawString(40, 750, 'Startup Name: TechNova Tanzania')
        document.drawString(40, 730, 'Industry: FinTech')
        document.drawString(40, 710, 'Contact Email: hello@technova.example')
        document.save()
        upload = SimpleUploadedFile(
            'startup.pdf', pdf_content.getvalue(), content_type='application/pdf',
        )

        response = self.client.post(reverse('staff:data_import'), {
            'action': 'upload',
            'dataset': 'startup',
            'file': upload,
        })

        self.assertEqual(response.status_code, 200)
        batch = response.context['batch']
        self.assertContains(response, 'name="value_name"')
        self.assertContains(response, 'value="TechNova Tanzania"')
        self.assertContains(response, 'value="FinTech"')
        self.assertContains(response, 'value="hello@technova.example"')
        self.assertContains(response, 'name="map_name" value="Name"')

        confirm_data = {'action': 'confirm', 'batch_id': batch.pk}
        for field in (
            'name', 'startup_type', 'description', 'industry', 'website',
            'contact_email', 'phone', 'contact_person', 'contact_address',
            'source', 'status', 'contract_status', 'founded_date',
            'incubation_start', 'incubation_end', 'year_incubated',
        ):
            header = Startup._meta.get_field(field).verbose_name.title()
            confirm_data[f'map_{field}'] = header
            confirm_data[f'value_{field}'] = {
                'name': 'Corrected TechNova Tanzania',
                'industry': 'FinTech',
                'contact_email': 'hello@technova.example',
                'startup_type': 'public',
                'status': 'pending',
                'contract_status': 'draft',
            }.get(field, '')

        response = self.client.post(reverse('staff:data_import'), confirm_data)

        self.assertRedirects(response, f"{reverse('staff:data_import')}?batch={batch.pk}")
        startup = Startup.objects.get(name='Corrected TechNova Tanzania')
        self.assertEqual(startup.industry, 'FinTech')
        self.assertEqual(startup.contact_email, 'hello@technova.example')
        batch.refresh_from_db()
        self.assertEqual(batch.created_count, 1)
