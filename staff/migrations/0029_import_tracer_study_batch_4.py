from django.db import migrations
from django.utils.text import slugify


SOURCE = 'Buni and DTBi Tracer Study 2021'


def import_tracer_study(apps, schema_editor):
    from staff.startup_tracer_batch4 import BATCH_4, EXISTING_PROFILES, TRACER_URL

    Startup = apps.get_model('staff', 'Startup')
    TeamMember = apps.get_model('staff', 'StartupTeamMember')
    PublicSection = apps.get_model('staff', 'StartupPublicSection')
    StorySlide = apps.get_model('staff', 'StartupStorySlide')

    for record in BATCH_4:
        startup = Startup.objects.filter(name__iexact=record['name']).order_by('pk').first()
        if startup is None:
            base_slug = slugify(record['name']) or 'startup'
            slug, suffix = base_slug, 1
            while Startup.objects.filter(slug=slug).exists():
                suffix += 1
                slug = f'{base_slug}-{suffix}'
            startup = Startup(name=record['name'], slug=slug)
            startup.startup_type = 'public'
            startup.description = record['description']
            startup.industry = record['industry']
            startup.website = record['website']
            startup.contact_email = record.get('email', '')
            startup.phone = record.get('phone', '')
            startup.contact_person = ', '.join(record['contact'])
            startup.contact_address = 'Tanzania'
            startup.source = SOURCE
            startup.contract_status = 'draft'
            startup.status = 'active'
            startup.directory_visible = True
            startup.save()

        source_note = f'Source: {SOURCE}; {TRACER_URL}'
        PublicSection.objects.update_or_create(
            startup_id=startup.pk, title='About the startup',
            defaults={'body': record['description'], 'source_note': source_note, 'sort_order': 0},
        )
        PublicSection.objects.update_or_create(
            startup_id=startup.pk, title='Tracer study notes',
            defaults={
                'body': record['details'] + f" The source lists its status as {record['status_text']}.",
                'source_note': source_note, 'sort_order': 10,
            },
        )
        for index, name in enumerate(record['contact']):
            if not TeamMember.objects.filter(startup_id=startup.pk, name__iexact=name).exists():
                TeamMember.objects.create(startup_id=startup.pk, name=name, title='Contact person', sort_order=index)
        StorySlide.objects.get_or_create(
            startup_id=startup.pk, title='Startup profile',
            defaults={
                'caption': 'Illustrated profile artwork based on the tracer study.',
                'image_path': f'img/startups/{startup.slug}-cover.jpg',
                'alt_text': f'{startup.name} profile artwork', 'sort_order': 0,
            },
        )

    # Enrich matched records without changing their established profile data.
    for name, data in EXISTING_PROFILES.items():
        startup = Startup.objects.filter(name__iexact=name).order_by('pk').first()
        if startup is None:
            continue
        PublicSection.objects.update_or_create(
            startup_id=startup.pk, title=data['section_title'],
            defaults={
                'body': data['body'],
                'source_note': f'Source: {SOURCE}; {TRACER_URL}',
                'sort_order': 90,
            },
        )
        if data['website'] and not startup.website:
            startup.website = data['website']
            startup.save(update_fields=['website', 'updated_at'])
        for index, (person, title) in enumerate(data['contacts']):
            if not TeamMember.objects.filter(startup_id=startup.pk, name__iexact=person).exists():
                TeamMember.objects.create(startup_id=startup.pk, name=person, title=title, sort_order=20 + index)


class Migration(migrations.Migration):
    dependencies = [('staff', '0028_import_buni_nov2018_batch_3')]
    operations = [migrations.RunPython(import_tracer_study, migrations.RunPython.noop)]
