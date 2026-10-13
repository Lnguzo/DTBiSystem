from django.db import migrations
from django.utils.text import slugify


SOURCE = 'BUNI Hub Innovators Applications – STARTUPS tab'


def import_buni_hub_startups(apps, schema_editor):
    from staff.startup_buni_applications_batch5 import EXISTING, STARTUPS, WORKBOOK

    Startup = apps.get_model('staff', 'Startup')
    TeamMember = apps.get_model('staff', 'StartupTeamMember')
    PublicSection = apps.get_model('staff', 'StartupPublicSection')
    StorySlide = apps.get_model('staff', 'StartupStorySlide')

    for row in STARTUPS:
        startup = Startup.objects.filter(name__iexact=row['name']).order_by('pk').first()
        if startup is None:
            base_slug = slugify(row['name']) or 'startup'
            slug, suffix = base_slug, 1
            while Startup.objects.filter(slug=slug).exists():
                suffix += 1
                slug = f'{base_slug}-{suffix}'
            startup = Startup(name=row['name'], slug=slug)
            startup.startup_type = 'public'
            startup.description = row['description']
            startup.industry = row['industry']
            startup.website = row['website']
            startup.contact_email = row['email']
            startup.phone = row['phone']
            startup.contact_person = row['contact']
            startup.contact_address = 'Tanzania'
            startup.source = SOURCE
            startup.contract_status = 'draft'
            startup.status = 'active'
            startup.directory_visible = True
            startup.save()

        note = f'Source: {WORKBOOK}, STARTUPS worksheet.'
        PublicSection.objects.update_or_create(
            startup_id=startup.pk, title='About the startup',
            defaults={'body': row['description'], 'source_note': note, 'sort_order': 0},
        )
        references = ' '.join(row.get('refs', []))
        detail_note = f'Source: {WORKBOOK}, STARTUPS worksheet.'
        if references:
            detail_note += f' Further information: {references}'
        PublicSection.objects.update_or_create(
            startup_id=startup.pk, title='BUNI application details',
            defaults={
                'body': f"The application listed the venture status as {row['status']}. {row['extra']}",
                'source_note': detail_note[:255], 'sort_order': 10,
            },
        )
        if row['contact'] and not TeamMember.objects.filter(startup_id=startup.pk, name__iexact=row['contact']).exists():
            TeamMember.objects.create(startup_id=startup.pk, name=row['contact'], title='Contact person', sort_order=0)
        StorySlide.objects.get_or_create(
            startup_id=startup.pk, title='Startup profile',
            defaults={
                'caption': 'Illustrated profile artwork based on the BUNI Hub application.',
                'image_path': f'img/startups/{startup.slug}-cover.jpg',
                'alt_text': f'{startup.name} profile artwork', 'sort_order': 0,
            },
        )

    # Match product/company aliases already represented in the directory and
    # preserve richer existing profile content while filling missing contacts.
    for row in EXISTING:
        startup = Startup.objects.filter(name__iexact=row['name']).order_by('pk').first()
        if startup is None:
            startup = next((Startup.objects.filter(name__iexact=alias).order_by('pk').first() for alias in row['aliases'][1:] if Startup.objects.filter(name__iexact=alias).exists()), None)
        if startup is None:
            continue
        PublicSection.objects.update_or_create(
            startup_id=startup.pk, title='BUNI applications workbook (STARTUPS)',
            defaults={
                'body': row['description'],
                'source_note': f'Source: {WORKBOOK}, STARTUPS worksheet.',
                'sort_order': 100,
            },
        )
        changed = []
        for field, source_field in (('contact_email', 'email'), ('phone', 'phone'), ('website', 'website')):
            if row[source_field] and not getattr(startup, field):
                setattr(startup, field, row[source_field])
                changed.append(field)
        if changed:
            startup.save(update_fields=changed + ['updated_at'])
        if row['email'] and '@' not in startup.contact_person:
            for index, person in enumerate([p.strip() for p in startup.contact_person.split(',') if p.strip()]):
                if not TeamMember.objects.filter(startup_id=startup.pk, name__iexact=person).exists():
                    TeamMember.objects.create(startup_id=startup.pk, name=person, title='Contact person', sort_order=index)


class Migration(migrations.Migration):
    dependencies = [('staff', '0029_import_tracer_study_batch_4')]
    operations = [migrations.RunPython(import_buni_hub_startups, migrations.RunPython.noop)]
