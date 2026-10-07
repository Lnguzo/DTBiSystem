"""Source-backed DTBi startup directory records from the supplied workbook."""

STARTUP_CATALOG = [
    ("Manufacturing", "Nyirenda’s Company", "Develops prepaid water meters."),
    ("Manufacturing", "Guavay Company Limited", "Produces organic fertilizer and pharmaceutical solutions."),
    ("Manufacturing", "Bee Venom Sensor", "Develops a sensor device for collecting bee venom."),
    ("Manufacturing", "Neema Makundi", "Produces cashew nut almonds and markets them through ICT to local and external markets."),
    ("Manufacturing", "Hellena Sailas", "Recycles plastic waste into building material called EcoBricks."),
    ("ICT & Software", "Hashtech Tanzania Limited", "BodaBoda Locator: a SIM enabled motorcycle device with location tracking, alarm, SMS alerts, and a fuel system disable feature."),
    ("Fintech & E-commerce", "iGlobal Learning Agency", "Fintech and education technology solution."),
    ("Fintech & E-commerce", "DayOne Softcom Technologies", "The workbook describes MRECOM as a billing platform used for revenue collection in 15 local government authorities, and a related TAMISEMI platform for 18 municipalities."),
    ("Fintech & E-commerce", "Maxcom Africa Ltd", "Provides electronic payment and financial solutions through Max Malipo. The workbook reports operations in Rwanda and Burundi."),
    ("Fintech & E-commerce", "A-Trader", "Trading platform for the Dar es Salaam Stock Exchange."),
    ("Fintech & E-commerce", "Inets Co. Ltd", "Remote recharge application for prepaid electricity meters, usable from phones and computers."),
    ("Fintech & E-commerce", "Ports and Marine", "Mkombozi software for automating SACCO membership, credit, and daily operations."),
    ("Fintech & E-commerce", "StraightBook Limited", "Develops accounting software."),
    ("Fintech & E-commerce", "BR Solutions", "BEI SOKONI is an SMS based service providing farmers current retail and wholesale produce prices from major markets."),
    ("Fintech & E-commerce", "ARLZY Microsystems Limited", "Document management system for incoming and outgoing mail and other corporate documents."),
    ("Fintech & E-commerce", "Young Tech Limited", "Cashew nut documentation management system used in Lindi and Mtwara regions."),
    ("Fintech & E-commerce", "Touchtop Computers", "Asset management system for recording and controlling organizational assets."),
    ("Fintech & E-commerce", "Bashcom Enterprises", "Mobile donation system for payments, subscriptions, and contributions to religious institutions."),
    ("Education & EdTech", "ExamNet", "Education technology solution."),
    ("Education & EdTech", "UjuziNet", "Education technology and student administration system development."),
    ("Education & EdTech", "Shule Yetu.Com", "Education platform connecting parents and teachers to support children’s learning."),
    ("Education & EdTech", "African Great Thinkers", "Online examination system with an academic database and immediate results."),
    ("Education & EdTech", "Broadband Alliance - UhuruOne, COSTECH & Microsoft", "Broadband4Wote provided affordable wireless access to students and academic staff at higher learning institutions using TV White Spaces technology."),
    ("Tourism & Hospitality", "Kwe2Africa.com Ltd", "Safari Wallet."),
    ("Tourism & Hospitality", "Dropping Zone", "Respad Plus online accommodation booking portal for reservations at mid range hotels."),
    ("Transport & Logistics", "Twende Technologies", "Logistics solution."),
    ("Transport & Logistics", "Time Tickets (Dephics)", "Online event planning, organization, and ticketing system."),
    ("Construction & Real Estate", "Makazi.Com", "House design software and Pazisha marketing linkage."),
    ("Professional & Business Services", "Fix Chap", "On demand platform connecting customers with technicians."),
    ("Energy & Clean Technology", "Millennium Engineering Enterprise", "Solar energy solutions."),
    ("Creative Industries & Media", "Bongotoonz", "Animation, including television commercial graphics and short cartoons for television stations, corporations, and advertising agencies."),
    ("Creative Industries & Media", "BK Network (Kipaji App)", "For profit online talent platform."),
    ("Creative Industries & Media", "Moview Developers", "Application that gives African movie fans information about films and cinema halls."),
    ("Creative Industries & Media", "Hainess Faraja", "Creative animation for children."),
    ("Health & MedTech", "Digital Brain", "Cloud based knowledge management platform with patient management for health centres and distribution management."),
    ("Health & MedTech", "Derick Machango", "eHospital platform."),
    ("ICT & Software", "Scancode (T) Limited", "Tools for detecting counterfeit products, documents, and certificates."),
    ("ICT & Software", "Magila Technologies Limited", "Software and cyber security services."),
    ("ICT & Software", "SasaTech", "Software development and security auditing system."),
    ("ICT & Software", "Equipoint", "Fleet and fuel monitoring solution."),
    ("ICT & Software", "Aim Firms", "Online data backup and recovery solution."),
]

# More complete records from the workbook's Startup Details sheet. Contacts are
# stored in fields only shown to the startup owner and DTBi staff.
STARTUP_DETAILS = {
    "Nyirenda’s Company": {"website": "https://nyirenda.com", "year": 2021, "contract": "inactive", "founder": "Wilbroad Nyirenda", "role": "CEO", "email": "nyirendas@gmail.com", "phone": "+255789105606", "industry": "Manufacturing"},
    "Guavay Company Limited": {"website": "https://guavay.com", "year": 2014, "contract": "inactive", "founder": "Ahad Katera", "role": "CEO", "email": "info@hakikafertilizer.co.tz", "phone": "+255679759883", "industry": "Manufacturing", "web_note": "The company website presents Hakika organic and mineral-organic fertilizers."},
    "Bee Venom Sensor": {"website": "https://beeven.com", "year": 2021, "contract": "inactive", "founder": "Patrick Kitosi", "role": "CEO", "email": "info@kiwangwabiotech.co.tz", "phone": "+255791780408", "industry": "Manufacturing"},
    "Hashtech Tanzania Limited": {"website": "https://hashtech.com", "year": 2014, "contract": "inactive", "founder": "Zena Msonde", "role": "CEO", "email": "info@hashtec.co.tz", "phone": "+255736969594", "industry": "ICT & Software"},
    "ExamNet": {"website": "", "year": 2020, "contract": "inactive", "founder": "Moses Mbaga", "role": "CTO", "email": "", "phone": "+255719369936", "industry": "Education & EdTech"},
    "UjuziNet": {"website": "https://ujuzinet.co.tz/", "year": 2020, "contract": "inactive", "founder": "Aderald Urassa", "role": "CEO", "email": "info@funguo.org", "phone": "+255699365987", "industry": "Education & EdTech", "web_note": "The current UjuziNet site describes digital learning and related technology products."},
    "Shule Yetu.Com": {"website": "https://shuleyetu.com/", "year": 2021, "contract": "inactive", "founder": "Willium Ellia", "role": "CEO", "email": "info@shuleyetu.com", "phone": "+255733700679", "industry": "Education & EdTech"},
    "African Great Thinkers": {"website": "", "year": 2008, "contract": "inactive", "founder": "Boniphace Rutta", "role": "Managing Director", "email": "", "phone": "+255754362422", "industry": "Education & EdTech"},
    "Broadband Alliance - UhuruOne, COSTECH & Microsoft": {"website": "https://uhuruone.com", "year": 2009, "contract": "inactive", "founder": "Mihayo Wilmore", "role": "CEO", "email": "info@costech.or.tz", "phone": "+255738746511", "industry": "Education & EdTech"},
    "Kwe2Africa.com Ltd": {"website": "https://kwe2africa.com", "year": 2012, "contract": "inactive", "founder": "Eid(iddy) John", "role": "CTO", "email": "md@kwe2africa.com", "phone": "+255714527934", "industry": "Tourism & Hospitality"},
    "Dropping Zone": {"website": "https://www.droppingzone.co.tz/", "year": 2009, "contract": "inactive", "founder": "Ramadhani Issa", "role": "Software Developer", "email": "support@droppingzone.co.tz", "phone": "+255759880969", "industry": "Tourism & Hospitality", "web_note": "The current site describes Respad property management and accommodation services."},
    "Twende Technologies": {"website": "https://twende.co.tz/", "year": 2017, "contract": "inactive", "founder": "Justine Kashaigili", "role": "CEO", "email": "info@twende.co.tz", "phone": "+255696593420", "industry": "Transport & Logistics", "web_note": "The current site describes transport, parcel delivery, and related services."},
    "Time Tickets (Dephics)": {"website": "https://www.timetickets.co.tz/", "year": 2013, "contract": "inactive", "founder": "Josephat Mandara", "role": "CEO", "email": "info@dephics.co.tz", "phone": "+255677070995", "industry": "Transport & Logistics", "web_note": "BUNI’s tracer study identifies TIME Tickets as Dephics’ digital ticketing platform."},
}

# Years here are incubation years as listed by the workbook, never assumed
# company founding dates.
STARTUP_COHORT_YEAR_UPDATES = [(name, data["year"]) for name, data in STARTUP_DETAILS.items()]
