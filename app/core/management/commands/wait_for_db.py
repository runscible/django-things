import time 
from django.db import connections 
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """command that wait until the database are ready"""

    def handle(self, *args, **options):
        self.stdout.write('waiting database ...')
        db_connection = None

        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write('database unnabaliable , retrying')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('database connected!'))    
