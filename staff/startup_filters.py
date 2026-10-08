import re

from django.db.models import Q

from .models import Startup


STARTUP_INDUSTRY_CATEGORIES = (
    ('agriculture', 'Agriculture & Agritech', ('agriculture', 'agri', 'agribusiness', 'farming', 'livestock')),
    ('biotechnology', 'Biotechnology & Life Sciences', ('biotech', 'biotechnology', 'life science', 'laboratory')),
    ('construction', 'Construction & Real Estate', ('construction', 'real estate', 'property', 'building')),
    ('creative', 'Creative Industries & Media', ('creative', 'media', 'film', 'design', 'animation', 'publishing')),
    ('education', 'Education & EdTech', ('education', 'edtech', 'edu-tech', 'e-learning', 'learning', 'training')),
    ('energy', 'Energy & Clean Technology', ('energy', 'renewable', 'solar', 'clean technology', 'cleantech')),
    ('finance', 'Financial Services & FinTech', ('financial', 'finance', 'fintech', 'banking', 'payments', 'insurance')),
    ('food', 'Food & Beverage', ('food', 'beverage', 'food processing')),
    ('health', 'Health & MedTech', ('health', 'medical', 'medtech', 'pharma', 'wellness')),
    ('ict', 'ICT & Software', ('ict', 'software', 'information technology', 'telecommunications', 'computer systems', 'cybersecurity')),
    ('manufacturing', 'Manufacturing & Industry', ('manufacturing', 'industrial', 'engineering', 'fabrication')),
    ('professional', 'Professional & Business Services', ('professional services', 'business services', 'consulting')),
    ('retail', 'Retail & E-commerce', ('retail', 'e-commerce', 'ecommerce', 'online marketplace')),
    ('social', 'Social Enterprise & Community Services', ('social enterprise', 'community services', 'non-profit', 'nonprofit')),
    ('tourism', 'Tourism & Hospitality', ('tourism', 'hospitality', 'travel', 'hotel')),
    ('transport', 'Transport & Logistics', ('transport', 'logistics', 'mobility', 'delivery')),
    ('water', 'Water & Sanitation', ('water', 'sanitation', 'waste management')),
)


def _sector_keyword_pattern(keyword):
    """Anchor a sector keyword to its left word edge only."""
    return r'(?<![A-Za-z])' + re.escape(keyword)


def sector_query(sector):
    """Return an industry query matching one configured sector."""
    query = Q()
    for keyword in sector[2]:
        query |= Q(industry__iregex=_sector_keyword_pattern(keyword))
    return query


def industry_matches_sector_keywords(industry_text, keywords):
    """Check an industry label for a configured keyword at a left word edge."""
    return any(re.search(_sector_keyword_pattern(keyword), industry_text) for keyword in keywords)


def apply_startup_directory_filters(queryset, params):
    """Apply the shared startup directory search and filter parameters."""
    startup_type = params.get('type', '').strip().lower()
    if startup_type in {'public', 'individual'}:
        queryset = queryset.filter(startup_type=startup_type)

    search_query = params.get('q', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(industry__icontains=search_query)
            | Q(description__icontains=search_query) | Q(source__icontains=search_query)
        )

    industry_filter = params.get('industry', '').strip()
    if industry_filter.startswith('sector:'):
        sector_key = industry_filter.split(':', 1)[1]
        sector = next((item for item in STARTUP_INDUSTRY_CATEGORIES if item[0] == sector_key), None)
        if sector:
            queryset = queryset.filter(sector_query(sector))
    elif industry_filter:
        raw_industry = industry_filter.split(':', 1)[1] if industry_filter.startswith('industry:') else industry_filter
        queryset = queryset.filter(industry__iexact=raw_industry)

    status_filter = params.get('status', '').strip().lower()
    if status_filter in dict(Startup.STATUS_CHOICES):
        queryset = queryset.filter(status=status_filter)

    return queryset
