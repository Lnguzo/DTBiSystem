import re
import unicodedata
from django.core.management.base import BaseCommand
from django.db import transaction
from staff.models import Startup
from staff.startup_catalog import STARTUP_CATALOG, STARTUP_COHORT_YEAR_UPDATES


def normalized_name(value):
    value = value.casefold()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", value)


class Command(BaseCommand):
    help = "Add or update startup document records without hiding unrelated profiles."

    @transaction.atomic
    def handle(self, *args, **options):
        years = {normalized_name(name): year for name, year in STARTUP_COHORT_YEAR_UPDATES}
        records = {}
        for item in Startup.objects.order_by("pk"):
            records.setdefault(normalized_name(item.name), item)
        seen, created, updated = set(), 0, 0
        for category, name, description in STARTUP_CATALOG:
            key = normalized_name(name)
            if not key or key in seen:
                continue
            seen.add(key)
            item = records.get(key)
            if item is None:
                item = Startup(name=name)
                created += 1
            else:
                updated += 1
            item.startup_type = "public"
            item.description = description
            item.industry = category
            item.source = "startup.docx"
            item.directory_visible = True
            item.status = "active"
            if key in years:
                item.year_incubated = years[key]
            item.save()
            records[key] = item
        visible = Startup.objects.filter(directory_visible=True).count()
        self.stdout.write(self.style.SUCCESS(
            f"Processed {len(seen)} document organizations; created {created}, updated {updated}; "
            f"{visible} profiles visible. Unrelated profiles were preserved."
        ))