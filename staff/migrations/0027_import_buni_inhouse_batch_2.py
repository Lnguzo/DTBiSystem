from django.db import migrations
from django.utils.text import slugify


SOURCE = 'BUNI In-House Applications Batch 2'


def import_buni_startups(apps, schema_editor):
    from staff.startup_inhouse_batch2 import BATCH_2

    Startup = apps.get_model('staff', 'Startup')
    TeamMember = apps.get_model('staff', 'StartupTeamMember')
    PublicSection = apps.get_model('staff', 'StartupPublicSection')
    StorySlide = apps.get_model('staff', 'StartupStorySlide')

    for record in BATCH_2:
        startup = Startup.objects.filter(name__iexact=record['name']).order_by('pk').first()
        if startup is not None and startup.source != SOURCE:
            # Preserve pre-existing profiles and avoid creating duplicates.
            continue
        if startup is None:
            base_slug = slugify(record['name']) or 'startup'
            slug = base_slug
            suffix = 1
            while Startup.objects.filter(slug=slug).exists():
                suffix += 1
                slug = f'{base_slug}-{suffix}'
            startup = Startup(name=record['name'], slug=slug)

        startup.name = record['name']
        startup.startup_type = 'public'
        startup.description = record['description']
        startup.industry = record['industry']
        startup.website = record['website']
        startup.contact_email = record['email']
        startup.phone = record['phone']
        startup.contact_person = record['contact']
        startup.contact_address = record['address']
        startup.source = SOURCE
        startup.year_incubated = record['year_incubated']
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
        TeamMember.objects.update_or_create(
            startup_id=startup.pk,
            name=record['contact'],
            defaults={'title': 'Contact person', 'bio': '', 'sort_order': 0},
        )
        StorySlide.objects.update_or_create(
            startup_id=startup.pk,
            title='Startup profile',
            defaults={
                'caption': 'Illustrated profile artwork based on the startup application.',
                'image_path': f'img/startups/{startup.slug}-cover.jpg',
                'alt_text': f"{startup.name} profile artwork",
                'sort_order': 0,
            },
        )


def remove_buni_startups(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    Startup.objects.filter(source=SOURCE).delete()


class Migration(migrations.Migration):
    dependencies = [('staff', '0026_import_boostup_batch_1')]
    operations = [migrations.RunPython(import_buni_startups, remove_buni_startups)]
