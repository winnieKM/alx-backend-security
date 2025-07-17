import logging
from ip2geotools.databases.noncommercial import DbIpCity
from django.http import HttpResponseForbidden
from .models import BlockedIP

logger = logging.getLogger(__name__)

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        ip = self.get_client_ip(request)
        
        # Blocked IP check
        if BlockedIP.objects.filter(ip_address=ip).exists():
            logger.warning(f"Blocked IP tried to access: {ip}")
            return HttpResponseForbidden("Forbidden")

        # Geolocation
        try:
            response = DbIpCity.get(ip, api_key='free')
            location = f"{response.city}, {response.region}, {response.country}"
            logger.info(f"Request from IP: {ip} - Location: {location}")
        except Exception as e:
            logger.error(f"Error retrieving location for IP {ip}: {str(e)}")

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
