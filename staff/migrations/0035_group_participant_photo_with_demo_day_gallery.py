from django.db import migrations


def group_photo_with_main_gallery(apps, schema_editor):
    Cohort = apps.get_model('staff', 'TalentPoolCohort')
    Event = apps.get_model('staff', 'TalentPoolEvent')
    Photo = apps.get_model('staff', 'TalentPoolPhoto')

    cohort = Cohort.objects.filter(slug='talent-pool-2026').first()
    if not cohort:
        return

    gallery_event = Event.objects.filter(
        cohort_id=cohort.pk,
        title='Talent Pool 2026 Demo Day',
    ).first()
    if not gallery_event:
        return

    photo = Photo.objects.filter(
        image_path='img/talent-pool/2026/talent-pool-2026-participants-session.jpg',
    ).first()
    if photo:
        photo.event_id = gallery_event.pk
        photo.save(update_fields=['event'])

    separate_event = Event.objects.filter(
        cohort_id=cohort.pk,
        title='Talent Pool Participant Session',
    ).first()
    if separate_event and not separate_event.photos.exists():
        separate_event.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('staff', '0034_add_talent_pool_participant_session_photo'),
    ]

    operations = [
        migrations.RunPython(group_photo_with_main_gallery, migrations.RunPython.noop),
    ]
