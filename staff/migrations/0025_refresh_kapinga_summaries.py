from django.db import migrations


SUMMARIES = {
    'nyirendas-company': (
        "Develops locally made prepaid water meters. FUNGUO reports that the solution is being piloted to improve transparency, reduce revenue losses, and strengthen water service delivery.",
        'https://nyirenda.com',
        'FUNGUO programme profile: https://funguo.org/updated/2025/05/05/',
    ),
    'guavay-company-limited': (
        'Founded in 2014, Guavay produces and distributes crop-specific organic and mineral-organic fertilizers, with a stated focus on improving soil health for African farmers.',
        'https://guavay.odoo.com/',
        'Company website: https://guavay.odoo.com/',
    ),
    'bee-venom-sensor': (
        'Patrick Kitosi developed solar-powered bee-venom harvesting equipment. A 2026 report says the machines are designed to collect venom without harming bees and identifies his company as Sensor Tanzania Ltd.',
        'https://beeven.com',
        'The Guardian (IPP Media), 26 Aug 2026: https://ippmedia.com/the-guardian/business/read/how-a-young-tanzanian-engineer-built-a-bee-venom-machine-2026-08-26-140038',
    ),
    'hashtech-tanzania-limited': (
        'HashTech builds mobility and tracking technology, including GPS tracking, electronic bus ticketing, ride-hailing, and software services. Its MySafari product supports digital travel ticketing.',
        'https://hashtech.co.tz/',
        'HashTech website: https://hashtech.co.tz/',
    ),
    'examnet': (
        "A mobile and web learning platform for Tanzania's primary learners, with curriculum-aligned practice exams, bilingual study tools, AI-supported tutoring, and feedback.",
        'https://examnet.net/',
        'Company website: https://examnet.net/',
    ),
    'ujuzinet': (
        'UjuziNet offers e-learning and a portfolio of software services, including AdBox Africa marketing automation, EMA business management, Hospito telemedicine, and Agrihubs farm management.',
        'https://ujuzinet.co.tz/',
        'UjuziNet company profile: https://www.linkedin.com/company/ujuzinet/',
    ),
    'shule-yetucom': (
        "ShuleYetu's school information platform combines school management, joint examinations, NECTA performance analysis, and fee management, with public school data tools and digital textbooks.",
        'https://shuleyetu.co.tz/',
        'Company website: https://shuleyetu.co.tz/',
    ),
    'african-great-thinkers': (
        'Online examination system with an academic database that lets students take exams and receive their scores.',
        '',
        'Source: kapinga.ods; no current company website located.',
    ),
    'broadband-alliance-uhuruone-costech-microsoft': (
        'Broadband4Wote was a pilot by UhuruOne, COSTECH, and Microsoft to provide affordable wireless broadband to university students and faculty using TV white spaces.',
        'https://uhuruone.com',
        'Microsoft, 8 May 2013: https://news.microsoft.com/source/2013/05/08/microsoft-partners-with-tanzania-commission-for-science-and-technology-and-uhuruone-to-bring-cutting-edge-broadband-access-windows-8-devices-and-technology-skills-to-local-universities/',
    ),
    'kwe2africacom-ltd': (
        'Safari Wallet was designed to help Tanzanian travelers plan holidays and pay for travel in instalments; it was developed by the travel company Kwetu Africa.',
        'https://kwe2africa.com',
        'Impact Tech Tanzania annual report: https://tmc.co.tz/wp-content/uploads/2025/01/Annual-Report_Promoting-Impact-Tech-Tanzania-2021.pdf?download=2778',
    ),
    'dropping-zone': (
        'A hospitality software company developing Respad 5, a property management system, and Spear, a tour-operator management system for bookings and itineraries.',
        'https://www.droppingzone.co.tz/',
        'Company website: https://www.droppingzone.co.tz/',
    ),
    'twende-technologies': (
        'A Tanzania mobility platform for boda, car, and bajaji rides, parcel delivery with live tracking, vendor sales, and an e-bike service.',
        'https://twende.co.tz/',
        'Company website: https://twende.co.tz/',
    ),
    'time-tickets-dephics': (
        "TiME Tickets is Dephics' event ticketing platform, providing flexible ticket purchase options and support for event organizers and attendees.",
        'https://tt.dephics.net/',
        'Product website: https://tt.dephics.net/',
    ),
}


def refresh_summaries(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    Section = apps.get_model('staff', 'StartupPublicSection')

    for slug, (description, website, source_note) in SUMMARIES.items():
        startup = Startup.objects.filter(slug=slug, source='kapinga.ods').first()
        if startup is None:
            continue
        startup.description = description
        startup.website = website
        startup.save(update_fields=['description', 'website'])
        Section.objects.filter(startup_id=startup.pk, title='Products and services').delete()
        Section.objects.update_or_create(
            startup_id=startup.pk,
            title='About the startup',
            defaults={
                'body': description,
                'source_note': source_note,
                'sort_order': 0,
            },
        )


class Migration(migrations.Migration):
    dependencies = [('staff', '0024_enrich_kapinga_profiles')]
    operations = [migrations.RunPython(refresh_summaries, migrations.RunPython.noop)]
