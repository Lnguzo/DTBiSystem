from django.db import migrations


ARTICLE_URL = (
    'https://startupafricaroadtrip.com/2025/05/26/'
    'smart-darasa-building-a-movement-for-inclusive-education/'
)


def update_smartdarasa_from_2025_article(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    StartupPublicSection = apps.get_model('staff', 'StartupPublicSection')
    startup = Startup.objects.filter(slug='smartdarasa').first()
    if not startup:
        return

    startup.website = 'https://smartdarasa.com'
    startup.save(update_fields=['website'])

    StartupPublicSection.objects.update_or_create(
        startup=startup,
        title='Product update and reported reach (May 2025)',
        defaults={
            'body': (
                'A Startup Africa Roadtrip interview published 26 May 2025 describes '
                'Smart Darasa as an offline-first learning platform for schools with '
                'limited connectivity. It reports that a new platform version launched '
                'in June 2024 with enhanced augmented-reality features, mobile apps and '
                'a free offline learning tool. The article says Smart Darasa merged '
                'with Smartcore to form Ekima Company Ltd, which it reports was then '
                'reaching over 500,000 students and teachers in 297 schools across '
                'Tanzania. These reach figures and the company relationship are '
                'attributed to that article and reflect its May 2025 report.'
            ),
            'source_note': f'Startup Africa Roadtrip interview, 26 May 2025: {ARTICLE_URL}',
            'sort_order': 45,
        },
    )
    StartupPublicSection.objects.update_or_create(
        startup=startup,
        title='Startup Africa Roadtrip and strategy',
        defaults={
            'body': (
                'The interview identifies founder Elias Elisante as a participant in '
                'the 2023 Startup Africa Roadtrip in Kigali, Rwanda. Elias says the '
                'programme informed a rethink of Smart Darasa’s go-to-market strategy '
                'and strategic partnerships, and encouraged an ecosystem-level vision '
                'for inclusive education.'
            ),
            'source_note': f'Startup Africa Roadtrip interview, 26 May 2025: {ARTICLE_URL}',
            'sort_order': 75,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('staff', '0020_smartdarasa_public_story_updates'),
    ]

    operations = [
        migrations.RunPython(update_smartdarasa_from_2025_article, migrations.RunPython.noop),
    ]
