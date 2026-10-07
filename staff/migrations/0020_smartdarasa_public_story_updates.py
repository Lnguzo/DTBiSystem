from django.db import migrations


def update_smartdarasa_public_story(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    StartupPublicSection = apps.get_model('staff', 'StartupPublicSection')
    startup = Startup.objects.filter(slug='smartdarasa').first()
    if not startup:
        return

    StartupPublicSection.objects.update_or_create(
        startup=startup,
        title='The problem',
        defaults={
            'body': (
                'The brochure describes a gap between theoretical STEM lessons and practical knowledge. '
                'It claims that more than 70% of schools have no laboratory or an under-equipped one, '
                'and identifies teacher shortages, uneven access to training and limited technology '
                'integration as barriers to students’ learning.'
            ),
            'source_note': 'Claims transcribed from the supplied SmartDarasa brochure; publication date not shown.',
            'sort_order': 10,
        },
    )
    StartupPublicSection.objects.update_or_create(
        startup=startup,
        title='The solution',
        defaults={
            'body': (
                'SmartDarasa presents classroom concepts through interactive 2D content, 360-degree '
                '3D models, online laboratory simulations and augmented reality. The brochure says '
                'teachers can use the platform to explain complex concepts and students can explore '
                'practical experiments remotely. It claims teachers can save more than 60% of '
                'preparation work and costs, and that simulations can support retention of up to '
                '90% after two weeks; these are claims in the source, not independently verified results.'
            ),
            'source_note': 'Product benefits as claimed in the supplied SmartDarasa brochure.',
            'sort_order': 20,
        },
    )
    StartupPublicSection.objects.update_or_create(
        startup=startup,
        title='Go-to-market approach',
        defaults={
            'body': (
                'The brochure outlines school visits, paid advertising, social and traditional media, '
                'and partnerships with teacher-training institutions. It names the University of '
                'Dodoma and the Dar es Salaam University College of Education as institutions that '
                'had shown interest in using SmartDarasa as a teaching aid. It also describes working '
                'with teachers and providing referral promo codes. This section records the brochure’s '
                'plan and reported interest, not independently verified current partnerships.'
            ),
            'source_note': 'Marketing plan and institutional interest stated in the supplied brochure.',
            'sort_order': 85,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0019_startup_contact_address_startup_contact_person'),
    ]

    operations = [
        migrations.RunPython(update_smartdarasa_public_story, migrations.RunPython.noop),
    ]
