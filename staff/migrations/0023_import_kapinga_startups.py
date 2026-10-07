from django.db import migrations, models
from django.utils.text import slugify


def import_startups(apps, schema_editor):
    from staff.startup_ods_catalog import STARTUPS

    Startup = apps.get_model('staff', 'Startup')
    TeamMember = apps.get_model('staff', 'StartupTeamMember')
    PublicSection = apps.get_model('staff', 'StartupPublicSection')

    for record in STARTUPS:
        startup = Startup.objects.filter(name__iexact=record['name']).order_by('pk').first()
        if startup is None:
            startup = Startup(name=record['name'])
        if not startup.slug:
            base_slug = slugify(record['name']) or 'startup'
            slug = base_slug
            suffix = 1
            while Startup.objects.exclude(pk=startup.pk).filter(slug=slug).exists():
                suffix += 1
                slug = f'{base_slug}-{suffix}'
            startup.slug = slug

        startup.startup_type = record['type']
        startup.description = record['description']
        startup.industry = record['industry']
        startup.website = record['website']
        startup.year_incubated = record['year']
        startup.contract_status = record['contract']
        startup.contact_person = record['founder']
        startup.contact_email = ''
        startup.phone = record['phone']
        startup.source = 'kapinga.ods'
        startup.directory_visible = True
        startup.status = 'active'
        startup.save()

        if record['description']:
            PublicSection.objects.update_or_create(
                startup_id=startup.pk,
                title='About the startup',
                defaults={
                    'body': record['description'],
                    'source_note': 'Source: kapinga.ods.',
                    'sort_order': 0,
                },
            )
        web_note = record.get('web_note')
        if web_note:
            PublicSection.objects.update_or_create(
                startup_id=startup.pk,
                title='Products and services',
                defaults={
                    'body': web_note,
                    'source_note': f"Source: {record['website']}",
                    'sort_order': 1,
                },
            )
        TeamMember.objects.update_or_create(
            startup_id=startup.pk,
            name=record['founder'],
            defaults={
                'title': record['role'],
                'bio': '',
                'sort_order': 0,
            },
        )


def remove_imported_startups(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    Startup.objects.filter(source='kapinga.ods').delete()


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
        migrations.AlterField(
            model_name='startupstatushistory',
            name='contract_status',
            field=models.CharField(blank=True, choices=[
                ('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'),
                ('expired', 'Expired'), ('terminated', 'Terminated'),
            ], max_length=20),
        ),
        migrations.RunPython(import_startups, remove_imported_startups),
    ]
