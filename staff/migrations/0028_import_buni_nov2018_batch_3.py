from datetime import date

from django.db import migrations
from django.utils.text import slugify


SOURCE = 'BUNI Nov 2018 Startup List Batch 3'


def import_nov2018_startups(apps, schema_editor):
    from staff.startup_buni_nov2018_batch3 import BATCH_3

    Startup = apps.get_model('staff', 'Startup')
    TeamMember = apps.get_model('staff', 'StartupTeamMember')
    PublicSection = apps.get_model('staff', 'StartupPublicSection')
    StorySlide = apps.get_model('staff', 'StartupStorySlide')

    for record in BATCH_3:
        startup = Startup.objects.filter(name__iexact=record['name']).order_by('pk').first()
        if startup is not None and startup.source != SOURCE:
            # Preserve any existing profile with this name rather than overwrite it.
            continue
        if startup is None:
            base_slug = slugify(record['name']) or 'startup'
            slug = base_slug
            suffix = 1
            while Startup.objects.filter(slug=slug).exists():
                suffix += 1
                slug = f'{base_slug}-{suffix}'
            startup = Startup(name=record['name'], slug=slug)

        contact_names = record['contacts']
        startup.name = record['name']
        startup.startup_type = 'public'
        startup.description = record['description']
        startup.industry = record['industry']
        startup.website = ''
        startup.contact_email = ''
        startup.phone = ''
        startup.contact_person = ', '.join(contact_names)
        startup.contact_address = record['address']
        startup.source = SOURCE
        startup.year_incubated = record['year_incubated']
        startup.incubation_start = date.fromisoformat(record['incubation_start'])
        startup.incubation_end = date.fromisoformat(record['incubation_end'])
        startup.contract_status = 'draft'
        startup.status = 'pending'
        startup.directory_visible = True
        startup.save()

        PublicSection.objects.update_or_create(
            startup_id=startup.pk,
            title='About the startup',
            defaults={
                'body': record['description'],
                'source_note': record['summary_source'],
                'sort_order': 0,
            },
        )
        for index, (title, body, source_note) in enumerate(record['sections'], start=1):
            PublicSection.objects.update_or_create(
                startup_id=startup.pk,
                title=title,
                defaults={
                    'body': body,
                    'source_note': source_note,
                    'sort_order': index * 10,
                },
            )
        for index, contact_name in enumerate(contact_names):
            TeamMember.objects.update_or_create(
                startup_id=startup.pk,
                name=contact_name,
                defaults={'title': 'Contact person', 'bio': '', 'sort_order': index},
            )
        StorySlide.objects.update_or_create(
            startup_id=startup.pk,
            title='Startup profile',
            defaults={
                'caption': 'Illustrated profile artwork based on the source document.',
                'image_path': f'img/startups/{startup.slug}-cover.jpg',
                'alt_text': f"{startup.name} profile artwork",
                'sort_order': 0,
            },
        )


def remove_nov2018_startups(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    Startup.objects.filter(source=SOURCE).delete()


class Migration(migrations.Migration):
    dependencies = [('staff', '0027_import_buni_inhouse_batch_2')]
    operations = [migrations.RunPython(import_nov2018_startups, remove_nov2018_startups)]
