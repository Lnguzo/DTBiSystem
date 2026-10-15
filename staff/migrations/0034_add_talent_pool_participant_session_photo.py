from django.db import migrations


def add_participant_session_photo(apps, schema_editor):
    Cohort = apps.get_model('staff', 'TalentPoolCohort')
    Event = apps.get_model('staff', 'TalentPoolEvent')
    Photo = apps.get_model('staff', 'TalentPoolPhoto')

    cohort = Cohort.objects.filter(slug='talent-pool-2026').first()
    if not cohort:
        return

    event, _ = Event.objects.update_or_create(
        cohort_id=cohort.pk,
        title='Talent Pool Participant Session',
        defaults={
            'event_type': 'workshop',
            'description': 'Participants take part in a Talent Pool learning session.',
            'is_published': True,
            'sort_order': 1,
        },
    )
    Photo.objects.update_or_create(
        event_id=event.pk,
        image_path='img/talent-pool/2026/talent-pool-2026-participants-session.jpg',
        defaults={
            'caption': 'Talent Pool participants during a learning session',
            'alt_text': 'Participants seated together and listening during a Talent Pool session.',
            'sort_order': 1,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('staff', '0033_add_private_innovator_records'),
    ]

    operations = [
        migrations.RunPython(add_participant_session_photo, migrations.RunPython.noop),
    ]
