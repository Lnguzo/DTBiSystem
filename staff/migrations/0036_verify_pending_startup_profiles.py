from django.db import migrations


VERIFIED_STARTUPS = {
    'agrobot': {
        'industry': 'AgriTech / AI Farmer Advisory',
        'website': 'http://www.agrobot.co.tz/',
        'description': (
            'A Tanzanian agricultural technology venture developing AI-supported farmer advice '
            'through SMS and chatbot channels, with information on crop diseases, farm inputs, '
            'and agricultural practices.'
        ),
        'section_title': 'Farmer advisory by SMS and chatbot',
        'section_body': (
            'Public company information describes AGROBOT as an AI-supported agricultural '
            'advisory service using SMS so farmers can ask practical farming questions. A 2026 '
            'Tanzania business report still cites the platform as an example of local digital '
            'agriculture. The service description is public; current coverage and availability '
            'should be confirmed with the team.'
        ),
        'source_note': 'Sources: AGROBOT company profile; DoingBusiness Tanzania, 2026 — https://www.linkedin.com/company/agrobotz/ ; https://doingbusiness.co.tz/how-ai-is-reshaping-tanzanias-business-landscape',
    },
    'abiri-innovations': {
        'industry': 'Livestock Safety / Satellite Tracking',
        'website': 'https://abiriinnovations.co.za/',
        'description': (
            'A South African technology startup developing satellite-powered livestock tracking '
            'and monitoring for rural households and smallholder farmers. Its current public '
            'profile describes field testing of tracking devices.'
        ),
        'section_title': 'Current focus: livestock protection',
        'section_body': (
            'Abiri Innovations’ current website describes a livestock-tracking product intended '
            'to help rural farmers monitor animals and reduce theft. The company says its devices '
            'are in field testing; this profile does not present them as a widely deployed product.'
        ),
        'source_note': 'Source: Abiri Innovations — https://abiriinnovations.co.za/ ; historical mapping profile: South African Department of Tourism.',
    },
    'african-child-project': {
        'industry': 'Social Enterprise / Education / Media',
        'website': 'https://africanchildprojects.org/',
        'description': (
            'A Tanzania-based social enterprise using storytelling and education to strengthen '
            'children’s confidence in African identity and connect African communities with the '
            'wider world. Its public work includes school connectivity and civic learning.'
        ),
        'section_title': 'Education, storytelling, and school connectivity',
        'section_body': (
            'The project’s current website lists education, storytelling, and civic initiatives. '
            'In June 2026, African Child Project and partners launched a school-connectivity '
            'initiative in Bagamoyo, with routers installed at six schools.'
        ),
        'source_note': 'Sources: African Child Projects — https://africanchildprojects.org/ ; AfrEd, 1 June 2026 — https://afred.org/2026/06/01/afred-african-child-project-and-basic-internet-launch-school-connectivity-initiative-in-bagamoyo/',
    },
    'agritechs': {
        'industry': 'AgriTech / Smart Hydroponics',
        'website': 'https://agritechs.co.tz/',
        'description': (
            'A Tanzanian agri-technology company developing smart hydroponic systems that combine '
            'soilless cultivation with sensors and connected technology. Its systems are intended '
            'to support controlled, climate-smart horticulture.'
        ),
        'section_title': 'Smart hydroponics',
        'section_body': (
            'The company’s documented product combines hydroponic structures with IoT technology '
            'for controlled horticulture. A 2024 Tanzania digital-agriculture report describes '
            'AgriTechs as serving larger farmers able to invest in the required systems.'
        ),
        'source_note': 'Source: Digital Frontiers, Tanzania digital-agriculture report — https://files.digitalfrontiersdai.com/media/documents/Tanzania_Report_External.pdf',
    },
    'cyber-kajumo-rigs': {
        'industry': 'Metal Fabrication / Upcycled Art / STEM',
        'website': 'https://bw.linkedin.com/company/kajumo',
        'description': (
            'A Botswana metal-fabrication venture that turns reclaimed metal into large-scale art, '
            'tourism landmarks, custom installations, and STEM learning pieces. Its work also '
            'includes welding, repairs, and fabrication.'
        ),
        'section_title': 'From reclaimed metal to public installations',
        'section_body': (
            'A July 2025 profile documented Cyber Kajumo Rigs building and installing a nine-metre '
            'robot sculpture at Dream View Farms in Botswana and described ongoing fabrication '
            'work. The company’s LinkedIn profile also describes its metal-art and STEM work.'
        ),
        'source_note': 'Sources: Batswana Entrepreneurs, 9 July 2025 — https://batswanaentrepreneurs.blogspot.com/2025/07/from-scrap-to-spectacle-botswanas-first.html ; Cyber Kajumo Rigs — https://bw.linkedin.com/company/kajumo',
    },
    'eastern-manual-drilling': {
        'industry': 'Water Access / Manual Drilling / Pumps',
        'website': 'https://emd-zambia.com/',
        'description': (
            'A Zambian cooperative providing manual borehole drilling and locally made, repairable '
            'water pumps for rural communities. Its public service information also covers well '
            'deepening and water-access solutions.'
        ),
        'section_title': 'Rural water-access services',
        'section_body': (
            'Eastern Manual Drilling’s website describes manual drilling and installation of '
            'simple, affordable, repairable pumps, and reports more than 700 customers. Zambia’s '
            'Water Resources Management Authority included the cooperative in its 2023 licensed '
            'drillers list.'
        ),
        'source_note': 'Sources: Eastern Manual Drilling — https://emd-zambia.com/ ; WARMA, 2023 licensed drillers — https://warma.org.zm/wp-content/uploads/2023/05/2023-Granted-Drillers1.pdf',
    },
    'fynhacker-limited': {
        'industry': 'Cybersecurity / Software / Web Hosting',
        'website': 'https://fynhacker.com/',
        'description': (
            'A Dar es Salaam technology company associated with web development, hosting, and '
            'cybersecurity services. Public business listings place its operations in Kigamboni.'
        ),
        'section_title': 'Technology and hosting services',
        'section_body': (
            'Public business profiles describe Fynhacker as a Tanzania-based web-development and '
            'hosting provider, with cybersecurity and managed technology services also listed. '
            'Confirm the current service catalogue directly with the company.'
        ),
        'source_note': 'Sources: Tanzapages Fynhacker Hosting listing — https://www.tanzapages.com/companies/software_company ; SoftwareWorld company profile — https://www.softwareworld.co/service/fynhacker-reviews/',
    },
    'greenbelt-energy': {
        'industry': 'Renewable Energy / Biogas',
        'website': 'https://gbezambia.com/',
        'description': (
            'A Zambian clean-energy company developing biogas systems and low-emission cooking '
            'solutions with farmers and local communities. Its public profile describes biogas '
            'production, smart cookstoves, and biodigester services.'
        ),
        'section_title': 'Biogas and clean cooking',
        'section_body': (
            'Greenbelt Energy’s current company profile describes work with farmers, women, and '
            'young people in Zambia to build a bioenergy ecosystem. It lists biogas and smart '
            'cookstoves among its clean-cooking solutions.'
        ),
        'source_note': 'Source: Greenbelt Energy company profile — https://www.linkedin.com/company/greenbelt-energy-corporation/ ; https://gbezambia.com/',
    },
    'impala-technologies': {
        'industry': 'E-commerce / Online Retail',
        'website': 'https://impala.co.tz/',
        'description': (
            'A Tanzanian online marketplace connecting shoppers with vendors across electronics, '
            'home goods, beauty, hardware, and other retail categories, with online payment and '
            'delivery options.'
        ),
        'section_title': 'Online marketplace serving Tanzania',
        'section_body': (
            'Impala’s live marketplace lists products for sale, seller onboarding, payment options, '
            'delivery information, customer support, and policies for current transactions.'
        ),
        'source_note': 'Source: Impala Shopping — https://impala.co.tz/',
    },
    'jicho-pori-tours-safaris-ltd': {
        'industry': 'Tourism / Safaris',
        'website': 'https://www.tourhq.com/guide/TZ69892/jicho-pori-tours-safaris-ltd',
        'description': (
            'A locally owned Tanzania tour operator offering wildlife safaris, beach holidays, '
            'mountain climbing, cultural and historical tours, transfers, and accommodation '
            'bookings. Its public operator listing is based in Arusha and accepts trip enquiries.'
        ),
        'section_title': 'Tours and safari enquiries',
        'section_body': (
            'The public TourHQ operator profile lists safari and travel services, identifies the '
            'company as licensed, and provides a trip-request form. Contact the operator to '
            'confirm dates, availability, and current itineraries.'
        ),
        'source_note': 'Source: TourHQ operator profile — https://www.tourhq.com/guide/TZ69892/jicho-pori-tours-safaris-ltd',
    },
    'kalahari-honey': {
        'industry': 'Agriculture / Honey / Sustainable Beekeeping',
        'website': 'http://www.kalaharihoney.com/',
        'description': (
            'A Botswana honey and beekeeping enterprise that works with rural farmers, processes '
            'and sells honey products, and promotes beehive-based approaches to livelihoods and '
            'human-wildlife coexistence.'
        ),
        'section_title': 'Honey products and sustainable beekeeping',
        'section_body': (
            'Botswana’s 2025 agriculture project-design report identifies Kalahari Honey as one '
            'of the country’s formal honey processors and traders. A December 2025 business '
            'listing shows recent product updates; the SEED enterprise profile describes its '
            'beekeeping and farmer-support model.'
        ),
        'source_note': 'Source: IFAD Botswana project-design report, 2025 — https://webapps.ifad.org/members/eb-seminars/2025-11-25-EB-Consultations/docs/EB-2025-146-R-3-Project-Design-Report.pdf',
    },
    'mathgenius': {
        'industry': 'EdTech / Mathematics Education',
        'website': 'https://mathgenius.co.tz/',
        'description': (
            'A Dar es Salaam education venture offering mathematics camps, workshops, clinics, '
            'testing, coaching, and online learning for primary and secondary students, with a '
            'focus on confidence and problem-solving.'
        ),
        'section_title': 'Mathematics learning programmes',
        'section_body': (
            'MathGenius Africa’s public company profile lists Mathcamp, workshops, clinics, '
            'testing, and online learning for schools and students in Tanzania.'
        ),
        'source_note': 'Source: MathGenius Africa — https://tz.linkedin.com/company/mathgenius-africa ; https://mathgenius.co.tz/',
    },
    'mohiri': {
        'industry': 'HR Tech / Employment Services',
        'website': 'https://www.linkedin.com/company/mohiribw/',
        'description': (
            'A Botswana employment service that shares matched job opportunities through job '
            'letters and SMS alerts. Its public company page continues to publish job notices '
            'and recruitment updates.'
        ),
        'section_title': 'Job matching and SMS alerts',
        'section_body': (
            'Mohiri’s public company page describes job alerts matched to a subscriber’s area and '
            'profile. Recent 2026 updates include job letters and recruitment notices, providing '
            'current evidence that the service remains in use.'
        ),
        'source_note': 'Source: Mohiri company page and 2026 updates — https://www.linkedin.com/company/mohiribw/',
    },
    'my-pregnancy-journey': {
        'industry': 'HealthTech / Maternal Health',
        'website': 'https://www.mypregnancyjourney.co.za/',
        'description': (
            'An African-made maternal-health app providing pregnancy and postpartum information, '
            'tracking tools, expert content, a digital journal, and access to health professionals '
            'and local support.'
        ),
        'section_title': 'Maternal-health app and resources',
        'section_body': (
            'The official website describes app features, expert resources, and support for '
            'pregnancy and motherhood. Google Play lists the app with 50,000+ downloads and an '
            'August 2026 update.'
        ),
        'source_note': 'Sources: My Pregnancy Journey — https://www.mypregnancyjourney.co.za/ ; Google Play, updated 13 Aug 2026 — https://play.google.com/store/apps/details?id=com.mypregnancyjourney.app',
    },
}


def update_verified_startups(apps, schema_editor):
    Startup = apps.get_model('staff', 'Startup')
    PublicSection = apps.get_model('staff', 'StartupPublicSection')
    StatusHistory = apps.get_model('staff', 'StartupStatusHistory')

    for slug, details in VERIFIED_STARTUPS.items():
        startup = Startup.objects.filter(slug=slug, status='pending').first()
        if startup is None:
            continue

        for field in ('industry', 'website', 'description'):
            setattr(startup, field, details[field])
        startup.status = 'active'
        startup.save()

        StatusHistory.objects.create(
            startup_id=startup.pk,
            status='active',
            contract_status=startup.contract_status or '',
        )
        PublicSection.objects.get_or_create(
            startup_id=startup.pk,
            title=details['section_title'],
            defaults={
                'body': details['section_body'],
                'source_note': details['source_note'],
                'sort_order': 10,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('staff', '0035_group_participant_photo_with_demo_day_gallery'),
    ]

    operations = [
        migrations.RunPython(update_verified_startups, migrations.RunPython.noop),
    ]
