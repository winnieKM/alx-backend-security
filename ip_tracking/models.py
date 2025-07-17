# ip_tracking/models.py

from django.db import models



class RequestLog(models.Model):
    # your existing fields
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.country}, {self.city} at {self.timestamp}"

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField(null=True, blank=True)
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - Blocked on {self.blocked_at}"
