from django.db import migrations
from django.utils.text import slugify


PROFILES = {
    'nyirendas-company': {
        'sections': [
            ('Product and pilot', "FUNGUO describes a locally developed prepaid water meter being piloted to improve billing transparency, reduce revenue losses, and strengthen water service delivery.", 'FUNGUO programme profile: https://funguo.org/updated/2025/05/05/'),
        ],
        'slides': [
            ('Prepaid water meter', 'A product image from a public listing attributed to Wilbroad Nyirenda. The company website could not be verified.', 'img/startups/official_sources/nyirenda_meter.webp', 'Prepaid water meter listed by Wilbroad Nyirenda'),
        ],
    },
    'guavay-company-limited': {
        'sections': [
            ('Products and approach', "Guavay presents its Hakika range of crop-specific organic and mineral-organic fertilizers. Its website describes the company as focused on soil health and African farmers.", 'Company website: https://guavay.odoo.com/'),
        ],
        'slides': [
            ('Farming and soil health', 'Image published on Guavay’s website.', 'img/startups/official_sources/guavay_hero.jpg', 'Farmer tending a crop field'),
            ('Guavay product', 'Product image published on Guavay’s website.', 'img/startups/official_sources/guavay_product.webp', 'Guavay fertilizer product'),
        ],
    },
    'bee-venom-sensor': {
        'sections': [
            ('Technology', 'A 2026 news report describes Patrick Kitosi’s solar-powered bee-venom harvesting equipment, designed to collect venom without harming the bees. The report says more than 117 machines had been made; this is a media-reported figure.', 'The Guardian (IPP Media), 26 Aug 2026: https://ippmedia.com/the-guardian/business/read/how-a-young-tanzanian-engineer-built-a-bee-venom-machine-2026-08-26-140038'),
        ],
        'slides': [
            ('Bee-venom harvesting machine', 'Photo from a news report about Patrick Kitosi’s bee-venom harvesting work; the image is editorial, not supplied by the startup.', 'img/startups/official_sources/bee_venom_feature.jpg', 'Patrick Kitosi with bee-venom harvesting equipment'),
        ],
    },
    'hashtech-tanzania-limited': {
        'sections': [
            ('Products and services', 'HashTech’s mobility and transport technology includes GPS tracking, electronic bus ticketing, ride-hailing, and parcel services. MySafari supports route search, seat selection, and digital bus-ticket bookings.', 'HashTech: https://hashtech.co.tz/ · MySafari: https://mysafari.co.tz/'),
        ],
        'slides': [
            ('MySafari passenger booking', 'Product image from the MySafari website, a HashTech service.', 'img/startups/official_sources/mysafari_gallery.jpeg', 'MySafari digital bus ticket booking interface'),
            ('MySafari agent tools', 'Agent product image from the MySafari website.', 'img/startups/official_sources/mysafari_agent.png', 'MySafari agent booking tool'),
        ],
    },
    'examnet': {
        'sections': [
            ('Learning platform', 'ExamNet offers curriculum-aligned practice exams for Tanzanian primary learners, with bilingual study tools, instant feedback, and AI-supported tutoring on web and mobile.', 'Company website: https://examnet.net/'),
        ],
        'slides': [
            ('Learning for primary students', 'Illustrative education image used on ExamNet’s website.', 'img/startups/official_sources/examnet_kids.jpg', 'Children studying together'),
            ('Family learning', 'Illustrative image used on ExamNet’s website.', 'img/startups/official_sources/examnet_family.jpg', 'Family supporting a learner'),
            ('Teacher support', 'Illustrative image used on ExamNet’s website.', 'img/startups/official_sources/examnet_teacher.jpg', 'Teacher supporting students'),
        ],
    },
    'ujuzinet': {
        'sections': [
            ('Product portfolio', 'UjuziNet’s company profile lists UJUZINET e-learning, AdBox Africa marketing automation, EMA enterprise management, Hospito telemedicine, and Agrihubs farm management.', 'UjuziNet company profile: https://www.linkedin.com/company/ujuzinet/'),
        ],
        'slides': [
            ('EMA business management', 'Official EMA product logo. EMA is listed in UjuziNet’s product portfolio.', 'img/startups/official_sources/ema_logo.png', 'EMA business management product logo'),
        ],
    },
    'shule-yetucom': {
        'sections': [
            ('School tools', 'ShuleYetu brings together school management, joint examinations, NECTA performance analysis, fee management, public school information, and digital textbooks.', 'Company website: https://shuleyetu.co.tz/'),
        ],
        'slides': [
            ('ShuleYetu platform', 'ShuleYetu logo from the company website.', 'img/startups/official_sources/shuleyetu_logo.png', 'ShuleYetu logo'),
        ],
    },
    'african-great-thinkers': {
        'sections': [
            ('Available information', 'The supplied startup register describes an online examination system with an academic database for students to take exams and receive scores. No current company website or verified product imagery was found.', 'Source: kapinga.ods; current website not located.'),
        ],
    },
    'broadband-alliance-uhuruone-costech-microsoft': {
        'sections': [
            ('Broadband4Wote pilot', 'A historical Microsoft, COSTECH, and UhuruOne initiative tested affordable wireless broadband using TV white spaces for university students and faculty. The source describes a pilot, not a current commercial service.', 'Microsoft, 8 May 2013: https://news.microsoft.com/source/2013/05/08/microsoft-partners-with-tanzania-commission-for-science-and-technology-and-uhuruone-to-bring-cutting-edge-broadband-access-windows-8-devices-and-technology-skills-to-local-universities/'),
        ],
    },
    'kwe2africacom-ltd': {
        'sections': [
            ('Safari Wallet', 'A published company profile describes Safari Wallet as a way for local travelers to plan holidays and pay in instalments. The Kwe2Africa website could not be verified as currently available.', 'Impact Tech Tanzania annual report: https://tmc.co.tz/wp-content/uploads/2025/01/Annual-Report_Promoting-Impact-Tech-Tanzania-2021.pdf?download=2778'),
        ],
    },
    'dropping-zone': {
        'sections': [
            ('Hospitality software', 'Respad 5 supports accommodation operations as a property management system. Spear is a tour-operator management system for bookings and itineraries.', 'Company website: https://www.droppingzone.co.tz/'),
        ],
        'slides': [
            ('Respad property management', 'Product screenshot published on Dropping Zone’s website.', 'img/startups/official_sources/dropping_respad_screenshot.png', 'Respad property-management interface'),
            ('Spear tour operations', 'Product screenshot published on Dropping Zone’s website.', 'img/startups/official_sources/dropping_spear_screenshot.png', 'Spear tour-operator interface'),
        ],
    },
    'twende-technologies': {
        'sections': [
            ('Mobility and delivery', 'Twende lists boda, car, and bajaji rides, parcel delivery with tracking, vendor services, e-bikes, and per-ride micro-insurance.', 'Company website: https://twende.co.tz/'),
        ],
        'slides': [
            ('Twende service area', 'Map visual published on Twende’s website.', 'img/startups/official_sources/twende_hero_map.webp', 'Map visual from Twende’s website'),
            ('Twende brand', 'Brand image published on Twende’s website.', 'img/startups/official_sources/twende_brand.jpg', 'Twende brand artwork'),
        ],
    },
    'time-tickets-dephics': {
        'sections': [
            ('Event ticketing', 'TiME Tickets provides online ticket purchasing and support for event organizers and attendees.', 'Product website: https://tt.dephics.net/'),
        ],
        'slides': [
            ('TiME Tickets by Dephics', 'Dephics company logo from its official product site.', 'img/startups/official_sources/dephics_logo.svg', 'Dephics logo'),
        ],
    },
}


def enrich_profiles(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    Section = apps.get_model('staff', 'StartupPublicSection')
    Slide = apps.get_model('staff', 'StartupStorySlide')

    for slug, data in PROFILES.items():
        startup = Startup.objects.filter(slug=slug).first()
        if startup is None:
            continue
        if slug == 'nyirendas-company':
            # The imported ODS name had a replacement character; repair it by slug.
            startup.name = "Nyirenda's Company"
            startup.save(update_fields=['name'])

        for order, (title, body, source_note) in enumerate(data.get('sections', []), start=1):
            Section.objects.update_or_create(
                startup_id=startup.pk,
                title=title,
                defaults={'body': body, 'source_note': source_note, 'sort_order': order * 10},
            )

        for order, (title, caption, image_path, alt_text) in enumerate(data.get('slides', [])):
            Slide.objects.update_or_create(
                startup_id=startup.pk,
                title=title,
                defaults={
                    'caption': caption,
                    'image_path': image_path,
                    'alt_text': alt_text,
                    'sort_order': order,
                },
            )


class Migration(migrations.Migration):
    dependencies = [('staff', '0023_import_kapinga_startups')]
    operations = [migrations.RunPython(enrich_profiles, migrations.RunPython.noop)]
