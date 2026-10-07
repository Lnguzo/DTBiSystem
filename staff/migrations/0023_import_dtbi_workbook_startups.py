from django.db import migrations, models
from django.utils.text import slugify


def import_startups(apps, schema_editor):
    # This data module is versioned with the project and mirrors the supplied
    # DTBi STARTUPS AND PROJECTS workbook's STARTUPS and Startup Details sheets.
    from staff.startup_catalog import STARTUP_CATALOG, STARTUP_DETAILS

    Startup = apps.get_model('staff', 'Startup')
    TeamMember = apps.get_model('staff', 'StartupTeamMember')
    PublicSection = apps.get_model('staff', 'StartupPublicSection')
    individual_names = {
        'neema makundi', 'hellena sailas', 'hainess faraja', 'derick machango',
    }

    for industry, name, description in STARTUP_CATALOG:
        startup = Startup.objects.filter(name__iexact=name).order_by('pk').first()
        if startup is None:
            startup = Startup(name=name)
        if not startup.slug:
            base_slug = slugify(name) or 'startup'
            slug = base_slug
            suffix = 1
            while Startup.objects.exclude(pk=startup.pk).filter(slug=slug).exists():
                suffix += 1
                slug = f'{base_slug}-{suffix}'
            startup.slug = slug
        details = STARTUP_DETAILS.get(name, {})
        startup.startup_type = 'individual' if name.casefold() in individual_names else 'public'
        startup.description = description
        startup.industry = details.get('industry', industry)
        startup.website = details.get('website', '')
        startup.source = 'DTBi STARTUPS AND PROJECTS workbook'
        startup.directory_visible = True
        startup.status = 'active'
        startup.year_incubated = details.get('year')
        startup.contract_status = details.get('contract', '')
        startup.contact_person = details.get('founder', '')
        startup.contact_email = details.get('email', '')
        startup.phone = details.get('phone', '')
        startup.save()

        PublicSection.objects.update_or_create(
            startup_id=startup.pk,
            title='About the startup',
            defaults={
                'body': description,
                'source_note': 'Source: DTBi STARTUPS AND PROJECTS workbook.',
                'sort_order': 0,
            },
        )
        web_note = details.get('web_note')
        if web_note and startup.website:
            PublicSection.objects.update_or_create(
                startup_id=startup.pk,
                title='Products and services',
                defaults={
                    'body': web_note,
                    'source_note': f'Source: {startup.website}',
                    'sort_order': 1,
                },
            )

        founder = details.get('founder')
        if founder:
            TeamMember.objects.update_or_create(
                startup_id=startup.pk,
                name=founder,
                defaults={
                    'title': details.get('role', ''),
                    'bio': '',
                    'sort_order': 0,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0022_startup_inquiries_and_public_opportunity_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='contract_status',
            field=models.CharField(blank=True, choices=[
                ('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'),
                ('expired', 'Expired'), ('terminated', 'Terminated'),
            ], default='draft', max_length=20),
        ),
        migrations.RunPython(import_startups, migrations.RunPython.noop),
    ]
