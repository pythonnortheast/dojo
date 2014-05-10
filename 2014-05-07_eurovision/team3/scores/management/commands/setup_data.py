from django.core.management.base import BaseCommand, CommandError
from scores.scripts import do_scores, import_countries

class Command(BaseCommand):
    help = 'Setup initial data'

    def handle(self, *args, **options):
        import_countries()
        do_scores()
        self.stdout.write('Successfully setup data')