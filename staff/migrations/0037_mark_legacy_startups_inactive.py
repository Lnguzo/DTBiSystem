from django.db import migrations


LEGACY_STARTUP_SLUGS = (
    'foodsasa',
    'sipho-group-company-limited',
    'lure',
    'tukuvi-network',
    'xtend-africa-ltd',
    'smarterads',
    'karata-technologies',
    'fiti-milele',
    'tuits',
    'the-lab',
    'sakab-holdings-pty-ltd',
    'jointpesa',
    'iot-radar',
    'guardian-gabriel',
    'agua-contada',
)


def mark_legacy_startups_inactive(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    StatusHistory = apps.get_model('staff', 'StartupStatusHistory')

    startups = Startup.objects.filter(slug__in=LEGACY_STARTUP_SLUGS, status='pending')
    for startup in startups.iterator():
        startup.status = 'inactive'
        startup.directory_visible = False
        startup.save(update_fields=['status', 'directory_visible', 'updated_at'])
        StatusHistory.objects.create(
            startup_id=startup.pk,
            status='inactive',
            contract_status=startup.contract_status or '',
        )


class Migration(migrations.Migration):
    dependencies = [
        ('staff', '0036_verify_pending_startup_profiles'),
    ]

    operations = [
        migrations.RunPython(mark_legacy_startups_inactive, migrations.RunPython.noop),
    ]
