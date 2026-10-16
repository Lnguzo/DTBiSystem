"""Import MAKISATU project and confidential programme records from an XLSX workbook."""

import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.utils.text import slugify

from staff.models import InnovatorProfile, UserProfile


User = get_user_model()
MAIN_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
NS = {'m': MAIN_NS}
STOP_WORDS = {'a', 'an', 'and', 'by', 'for', 'from', 'in', 'of', 'the', 'to', 'using', 'with'}
MILESTONE_COLUMNS = (('D', 'E'), ('F', 'G'), ('H', 'I'), ('J', 'K'))


def read_workbook_rows(path):
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise CommandError(f'Cannot read the XLSX file: {exc}') from exc
    with archive:
        try:
            shared_root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
            shared = [
                ''.join(text.text or '' for text in item.iter(f'{{{MAIN_NS}}}t'))
                for item in shared_root
            ]
            sheet = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
        except (KeyError, ET.ParseError) as exc:
            raise CommandError('The workbook is missing a readable first worksheet or shared strings.') from exc

        rows = []
        for row in sheet.findall('.//m:sheetData/m:row', NS):
            values = {}
            for cell in row.findall('m:c', NS):
                column = ''.join(char for char in cell.get('r', '') if char.isalpha())
                if not column:
                    continue
                if cell.get('t') == 's':
                    index = int(cell.findtext('m:v', default='0', namespaces=NS))
                    value = shared[index] if index < len(shared) else ''
                elif cell.get('t') == 'inlineStr':
                    value = ''.join(text.text or '' for text in cell.iter(f'{{{MAIN_NS}}}t'))
                else:
                    value = cell.findtext('m:v', default='', namespaces=NS)
                values[column] = str(value).strip()
            rows.append((int(row.get('r', '0')), values))
        return rows


def person_key(value):
    tokens = re.findall(r'[a-z0-9]+', (value or '').casefold())
    return ' '.join(token for token in tokens if len(token) > 1 and token not in {'dr', 'eng', 'mr', 'mrs', 'ms'})


def project_tokens(value):
    return {token for token in re.findall(r'[a-z0-9]+', (value or '').casefold()) if len(token) > 2 and token not in STOP_WORDS}


def same_person(left, right):
    left_tokens, right_tokens = set(person_key(left).split()), set(person_key(right).split())
    return bool(left_tokens and right_tokens and (left_tokens == right_tokens or left_tokens <= right_tokens or right_tokens <= left_tokens))


def same_project(left, right):
    left_tokens, right_tokens = project_tokens(left), project_tokens(right)
    if not left_tokens or not right_tokens:
        return (left or '').casefold().strip() == (right or '').casefold().strip()
    overlap = left_tokens & right_tokens
    if not overlap:
        return False
    if min(len(left_tokens), len(right_tokens)) <= 2 and overlap == min((left_tokens, right_tokens), key=len):
        return True
    return len(overlap) / len(left_tokens | right_tokens) >= 0.5


def parse_person_project(value, first_milestone, row_number):
    clean = (value or '').strip()
    if '(' in clean:
        person, _, project = clean.partition('(')
        person = person.strip()
        project = project.strip().rstrip(') ').strip()
    else:
        person = clean
        project = ''
    generic = {'procurement activity', 'stakeholder meeting', 'prototype improvement', 'na'}
    if not project and first_milestone and first_milestone.strip().casefold() not in generic:
        project = first_milestone.strip()
    if not project:
        project = f'{person} innovation'
    return person or f'Innovator {row_number}', project


class Command(BaseCommand):
    help = 'Import MAKISATU Innovator profiles, private contact details, and milestone records.'

    def add_arguments(self, parser):
        parser.add_argument('--file', required=True, help='Path to the source XLSX workbook.')

    def handle(self, *args, **options):
        workbook_path = Path(options['file'])
        if not workbook_path.is_file():
            raise CommandError(f'Workbook not found: {workbook_path}')
        rows = read_workbook_rows(workbook_path)
        imported = 0
        created = 0
        updated = 0
        linked_existing = list(InnovatorProfile.objects.select_related('user'))
        accounts_by_person = {}

        for row_number, cells in rows:
            raw_name = cells.get('B', '').strip()
            if not raw_name or raw_name.casefold() in {'name/ product', 'total'}:
                continue
            first_milestone = cells.get('D', '')
            person, project = parse_person_project(raw_name, first_milestone, row_number)
            email = cells.get('M', '').strip()
            milestones = []
            for index, (title_col, status_col) in enumerate(MILESTONE_COLUMNS, start=1):
                title = cells.get(title_col, '').strip()
                status = cells.get(status_col, '').strip()
                if title or status:
                    milestones.append(f'{index}. {title or "Not recorded"} | {status or "Not recorded"}')
            milestone_text = '\n'.join(milestones)

            match = next((profile for profile in linked_existing if
                same_person(profile.innovator_name, person)
                and same_project(profile.project_name, project)), None)
            if match is None:
                base_slug = slugify(f'{project}-{person}') or f'innovator-{row_number}'
                slug = base_slug
                suffix = 2
                while InnovatorProfile.objects.filter(slug=slug).exists():
                    slug = f'{base_slug}-{suffix}'
                    suffix += 1
                match = InnovatorProfile.objects.create(
                    innovator_name=person,
                    project_name=project,
                    slug=slug,
                    catalogue='makisatu',
                    description=f'{project} is an innovation project listed in the supplied MAKISATU records.',
                    is_published=True,
                )
                created += 1
                linked_existing.append(match)
            else:
                updated += 1

            key = person_key(person)
            user = accounts_by_person.get(key)
            if user is None:
                user = next((profile.user for profile in linked_existing
                    if profile.user_id and same_person(profile.innovator_name, person)
                    and UserProfile.objects.filter(user_id=profile.user_id, user_type='innovator').exists()), None)
            if user is None:
                user = self._create_innovator_account(person, email)
            accounts_by_person[key] = user

            match.innovator_name = person
            match.project_name = project
            match.catalogue = 'makisatu'
            match.contact_email = email
            match.phone_number = cells.get('N', '').strip()
            match.user = user
            match.entry_period = cells.get('C', '').strip()
            match.milestones_text = milestone_text
            match.programme_remarks = cells.get('L', '').strip()
            match.staff_recommendation = cells.get('O', '').strip()
            match.is_published = True
            if not match.description or match.description.endswith('supplied MAKISATU records.'):
                match.description = f'{project} is an innovation project listed in the supplied MAKISATU records.'
            match.save()

            # Keep the workbook phone in the private Innovator account's linked records.
            if match.phone_number:
                InnovatorProfile.objects.filter(user=user, phone_number='').update(phone_number=match.phone_number)
            imported += 1

        # Provision logins for profiles imported from the earlier Innovators email document too.
        all_profiles = list(InnovatorProfile.objects.select_related('user').order_by('innovator_name'))
        for profile in all_profiles:
            if profile.user_id:
                continue
            key = person_key(profile.innovator_name)
            user = accounts_by_person.get(key)
            if user is None:
                user = next((candidate.user for candidate in all_profiles
                    if candidate.user_id and same_person(candidate.innovator_name, profile.innovator_name)
                    and UserProfile.objects.filter(user_id=candidate.user_id, user_type='innovator').exists()), None)
            if user is None:
                user = self._create_innovator_account(profile.innovator_name, profile.contact_email)
            accounts_by_person[key] = user
            profile.user = user
            profile.save(update_fields=['user'])

        total_accounts = UserProfile.objects.filter(user_type='innovator').count()
        self.stdout.write(self.style.SUCCESS(
            f'Imported {imported} workbook entries ({created} new profiles, {updated} matched existing profiles). '
            f'{InnovatorProfile.objects.count()} total profiles now have {total_accounts} Innovator login accounts.'
        ))

    @staticmethod
    def _create_innovator_account(person, email):
        parts = (person or 'Innovator').split()
        first_name = parts[0]
        last_name = ' '.join(parts[1:])
        base = slugify(first_name) or 'innovator'
        username = base
        suffix = 2
        while True:
            if User.objects.filter(username__iexact=username).exists():
                username = f'{base}{suffix}'
                suffix += 1
                continue
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email if '@' in (email or '') else '',
                    password='123',
                    first_name=first_name,
                    last_name=last_name,
                )
                break
            except IntegrityError:
                username = f'{base}{suffix}'
                suffix += 1
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profile.user_type = 'innovator'
        user_profile.save(update_fields=['user_type'])
        return user
