from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Block an IP address by adding it to the BlockedIP list'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')

    def handle(self, *args, **kwargs):
        ip = kwargs['ip_address']

        if BlockedIP.objects.filter(ip_address=ip).exists():
            self.stdout.write(self.style.WARNING(f"IP {ip} is already blocked."))
        else:
            BlockedIP.objects.create(ip_address=ip)
            self.stdout.write(self.style.SUCCESS(f"IP {ip} has been blocked."))
