import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.contrib.gis.geoip2 import GeoIP2
from ip_tracking.models import BlockedIP, RequestLog

logger = logging.getLogger(__name__)

class IPTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the IP address
        ip = self.get_ip_address(request)

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access Denied: Your IP is blacklisted.")

        # Check cache first
        cached_data = cache.get(f"geoip:{ip}")
        if cached_data:
            country = cached_data.get('country')
            city = cached_data.get('city')
        else:
            try:
                geo = GeoIP2()
                data = geo.city(ip)
                country = data.get('country_name')
                city = data.get('city')
                # Cache for 24 hours
                cache.set(f"geoip:{ip}", {'country': country, 'city': city}, timeout=60 * 60 * 24)
            except Exception as e:
                logger.warning(f"GeoIP lookup failed for IP {ip}: {e}")
                country = None
                city = None

        # Log the request
        RequestLog.objects.create(ip_address=ip, country=country, city=city)

    def get_ip_address(self, request):
        """Gets client IP address, considering common headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
